from django.db import models
from django.contrib.auth import get_user_model

from articles.models import Article
from products.models import Product

# Create your models here.
_User = get_user_model()


class CommentManager(models.Manager):
    def confirmed(self):
        return self.get_queryset().filter(is_confirmed=True)


class Comment(models.Model):
    user = models.ForeignKey(
        _User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='کاربر نظر دهنده',
    )

    sender_fullname = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی ارسال کننده')
    date_posted = models.DateField(auto_now_add=True, verbose_name='تاریخ ارسال')
    text = models.TextField(max_length=300, verbose_name='متن پیام')
    is_confirmed = models.BooleanField(default=False, verbose_name='تایید شده/نشده')
    objects = CommentManager()

    @property
    def sender_avatar(self):
        return self.user.avatar_url()

    def __str__(self):
        return f'{self.sender_fullname}-{self.date_posted.strftime("%y %m %d")}'

    def add_comment(self, obj, user):
        raise NotImplementedError

    class Meta:
        abstract = True


class ArticleComment(Comment):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='مریط به مقاله',
        related_name='comments'
    )

    def add_comment(self, obj, user):
        self.article, self.user = obj, user
        self.save()


class ProductComment(Comment):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='مربوط به محصول',
        related_name='comments'
    )

    def add_comment(self, obj, user):
        self.product, self.user = obj, user
        self.save()
