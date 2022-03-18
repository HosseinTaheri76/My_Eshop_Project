from django.db import models
from utilties.models import SingletonModel
from .validators import validate_static_phone_number
from .uploaders import site_logo_uploader
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.

class SiteInfo(SingletonModel):
    name = models.CharField(max_length=50, default='سایت حسین', null=True, blank=True, verbose_name='اسم سایت')
    logo = models.ImageField(
        default='defaults/logo.png',
        upload_to=site_logo_uploader,
        null=True, blank=True,
        verbose_name='لوگوی سایت')
    phone = models.CharField(
        max_length=12,
        default='021-22712443',
        validators=[validate_static_phone_number],
        null=True, blank=True,
        verbose_name='شماره تلفن ثابت سایت'
    )
    email = models.EmailField(
        default='hosseintaheri76@gmail.com',
        null=True, blank=True,
        verbose_name='ایمیل سایت'
    )
    address = models.TextField(
        max_length=200,
        null=True, blank=True,
        verbose_name='آدرس شرکت'
    )
    short_about = models.TextField(
        max_length=100,
        null=True, blank=True,
        verbose_name='درباره ی ما مختصر'
    )
    copyright = models.TextField(
        max_length=100,
        null=True, blank=True,
        verbose_name='کپی رایت فوتر'
    )
    full_about = RichTextUploadingField(
        null=True, blank=True,
        verbose_name='محتوی صفحه درباره ی ما',
        config_name='advanced'
    )
    rules_page = RichTextUploadingField(
        null=True, blank=True,
        config_name='advanced',
        verbose_name='محتوی صفحه قوانین سایت'
    )

    class Meta:
        verbose_name = 'اطلاعات سایت'
        verbose_name_plural = 'اطلاعات سایت'

    def __str__(self):
        return 'اطلاعات سایت'

    def logo_url(self):
        try:
            return self.logo.url
        except ValueError:
            return '/media/defaults/logo.png'


class SocialMedia(models.Model):
    site_info = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, related_name='socials')
    name = models.CharField(max_length=50, verbose_name='نام رسانه اجتماعی')
    link = models.URLField(verbose_name='لینک')
    css_icon_class = models.CharField(max_length=50, verbose_name='کلاس css آیکون مربوطه')

    def __str__(self):
        return self.name
