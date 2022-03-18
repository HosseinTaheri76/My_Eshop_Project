from django.db import models
from ckeditor.fields import RichTextField
from .validators import validate_phone
from model_utils.tracker import FieldTracker


# Create your models here.

class UserMessage(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی')
    title = models.CharField(max_length=200, verbose_name='موضوع پیام')
    phone = models.CharField(max_length=14, validators=[validate_phone], verbose_name='شماره موبایل')
    email = models.EmailField(verbose_name='ایمیل')
    question_text = models.TextField(verbose_name='متن پیام')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پیام')
    is_answered = models.BooleanField(default=False, verbose_name='پاسخ داده شده/نشده')
    answer_text = RichTextField(config_name='advanced', verbose_name='پاسخ مدیر', null=True, blank=True)
    tracker = FieldTracker(fields=['is_answered'])

    def __str__(self):
        return f'{self.full_name}-{self.title}'

    class Meta:
        verbose_name = 'پیام کاربر'
        verbose_name_plural = 'پیام کاربران'
