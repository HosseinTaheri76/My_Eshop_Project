from django.contrib.auth import login
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from utilties.payment import start_payment
from django.views.generic import DetailView, FormView, UpdateView, ListView
from products.models import Product
from django.views import View
from .models import Order, OrderItem
from django.contrib import messages
from utilties.messaging import get_message
from .forms import RegisterOnOrderForm, OrderForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class CartPageView(DetailView):
    template_name = 'cart_page.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        order = Order.get_or_create_order(self.request)[1]
        if order.items.count():
            order.product_available(self.request)
        return order


class AddProductToCart(View):
    def get(self, request, product_id):
        created, order = Order.get_or_create_order(request)
        product = get_object_or_404(Product, id=product_id)
        if not product.is_available:
            messages.add_message(request, messages.ERROR, 'محصول مورد نظر موجود نمی باشد.')
            return redirect(request.META.get('HTTP_REFERER'))
        if not created and OrderItem.objects.filter(order=order, product=product).exists():
            messages.add_message(request, messages.ERROR, 'این محصول از قبل در سبد خرید شما موجود است.')
            return redirect(request.META.get('HTTP_REFERER'))
        OrderItem.objects.create(order=order, product=product, qty=1)
        messages.add_message(request, messages.SUCCESS, get_message('orders/added_to_cart').format(product.title))
        return redirect('cart')


class ChangeOrderItem(View):
    def get(self, request, action, item_id):
        if action not in ('add', 'reduce', 'delete'):
            return HttpResponseBadRequest(status=400)
        created, order = Order.get_or_create_order(request)
        if created:
            order.delete()
            return HttpResponseBadRequest(status=400)
        order_item = get_object_or_404(OrderItem, order=order, id=item_id)
        if action == 'add':
            result = order_item.add_qty()
            if not result:
                messages.add_message(request, messages.ERROR, get_message('orders/failed_add_qty_not_enough'))
        elif action == 'reduce':
            result = order_item.decrease_qty()
            if not result:
                return HttpResponseBadRequest(status=400)
        else:
            order_item.delete()
        return redirect('cart')


class OrderFormViewRegister(FormView):
    template_name = 'order_form_register.html'
    form_class = RegisterOnOrderForm

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            created, order = Order.get_or_create_order(self.request)
            if created:
                order.delete()
                return HttpResponseBadRequest(status=400)
            order.user = user
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']
            order.save()
        login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, get_message('authentication/account_created'))
        return start_payment(self.request, order.total_price, 'order')


class OrderFormAuthenticated(LoginRequiredMixin, UpdateView):
    template_name = 'order_form_user.html'
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        created, order = Order.get_or_create_order(self.request)
        if created:
            order.delete()
            return HttpResponseBadRequest(status=400)
        return order

    def get_initial(self):
        initial = {}
        user = self.request.user
        if user.address:
            initial['address'] = user.address
        if user.phone:
            initial['phone'] = user.phone
        return initial

    def form_valid(self, form):
        user = self.request.user
        form.save()
        initial = self.get_initial()
        if len(initial.keys()) < 2:
            if 'phone' not in initial:
                user.phone = form.cleaned_data['phone']
            if 'address' not in initial:
                user.address = form.cleaned_data['address']
            user.save()
        if 'gateway' in self.request.POST:
            return start_payment(self.request, self.get_object().total_price, 'order')
        elif 'credit' in self.request.POST:
            pay_credit_success = form.instance.pay_by_credit()
            if pay_credit_success:
                messages.add_message(self.request, messages.SUCCESS, get_message('orders/order_submitted'))
                return redirect('user_orders')
            messages.add_message(self.request, messages.ERROR, get_message('orders/insufficient_fuds'))
            return redirect('user_order_form')


class UserOrderListView(LoginRequiredMixin, ListView):
    template_name = 'user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.request.user.orders.filter(is_paid=True).order_by('-date_paid')


class UserOrderDetail(LoginRequiredMixin, DetailView):
    template_name = 'user_order_details.html'
    context_object_name = 'order'

    def get_queryset(self):
        return self.request.user.orders.filter(is_paid=True)

    def get_object(self, queryset=None):
        order_id = self.kwargs['order_id']
        try:
            return self.get_queryset().get(id=order_id)
        except Order.DoesNotExist:
            return HttpResponseNotFound(status=404)
