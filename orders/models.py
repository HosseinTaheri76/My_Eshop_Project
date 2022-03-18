from django.db import models, transaction, IntegrityError
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.http import HttpResponseRedirect
from django.urls import reverse

from products.models import Product
from model_utils.tracker import FieldTracker
from utilties.messaging import get_message
from django.contrib import messages as msg_module
from accounts.validators import validate_phone
from datetime import datetime
from random import randint


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='کاربر سفارش دهنده',
        related_name='orders',
    )
    order_no = models.IntegerField(unique=True, null=True, blank=True, verbose_name='شماره سفارش')
    date_paid = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ و زمان ثبت سفارش')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده/ نشده')
    status = models.CharField(max_length=200, null=True, blank=True, verbose_name='وضعیت سفارش')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس ارسال')
    phone = models.CharField(
        max_length=14,
        null=True,
        blank=True,
        verbose_name='شماره تماس',
        validators=[validate_phone])
    tracker = FieldTracker(['is_paid'])

    def get_absolute_url(self):
        return reverse('user_order_detail', args=(self.id,))

    def __str__(self):
        return f'{self.user.full_name}-{self.order_no}'

    @property
    def total_price(self):
        return sum(item.get_sum() for item in self.items.all())

    @classmethod
    def get_or_create_order(cls, request):
        if request.user.is_authenticated:
            try:
                return False, cls.objects.get(user=request.user, is_paid=False)
            except cls.DoesNotExist:
                return True, cls.objects.create(user=request.user, is_paid=False)
        else:
            try:
                order_id = request.session['order_id']
                return False, cls.objects.get(id=order_id)
            except (KeyError, cls.DoesNotExist):
                order = cls.objects.create()
                request.session['order_id'] = order.id
                return True, order

    def product_available(self, request):
        messages = []
        for item in self.items.all():
            product = item.product
            message = ''
            if not product.is_available:
                message = get_message('orders/product_not_available').format(product.title)
                item.delete()
            elif product.stock < item.qty:
                message = get_message('orders/not_enough_product').format(product.title)
                item.set_qty(product.stock)
            if message:
                messages.append(message)
        if messages:
            for msg in messages:
                msg_module.add_message(request, msg_module.WARNING, msg)
            return HttpResponseRedirect('cart')

    def process_order(self):
        with transaction.atomic():
            self.is_paid = True
            self.status = 'منتظر تایید'
            for item in self.items.all():
                item.product.buy(item.qty)
            self.date_paid = datetime.now()
            while True:
                try:
                    self.order_no = randint(10000, 99999)
                    self.save()
                    break
                except IntegrityError:
                    continue

    def pay_by_credit(self):
        check_user_credit = self.user.buy_by_credit(self.total_price)
        if check_user_credit:
            self.process_order()
            return True
        return False

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    qty = models.PositiveSmallIntegerField(verbose_name='تعداد محصول')

    def __str__(self):
        return f'{self.product.title} x {self.qty}'

    def get_sum(self):
        return self.product.price * self.qty

    def set_qty(self, number):
        self.qty = number
        self.save()

    def add_qty(self):
        if self.product.stock > self.qty:
            self.qty += 1
            self.save()
            return True
        return False

    def decrease_qty(self):
        if self.qty > 1:
            self.qty -= 1
            self.save()
            return True
        return False
