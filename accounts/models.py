from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .validators import validate_phone
from .uploaders import avatar_uploader


class UserManager(BaseUserManager):
    def _create_user(self, full_name, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, full_name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(full_name, email, password, **extra_fields)

    def create_superuser(self, full_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(full_name, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
    full_name = models.CharField(max_length=150, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(
        max_length=14,
        null=True,
        blank=True,
        validators=[validate_phone],
        verbose_name='شماره موبایل'
    )
    avatar = models.ImageField(
        upload_to=avatar_uploader,
        null=True,
        blank=True,
        verbose_name='عکس پروفایل'
    )
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    balance = models.PositiveBigIntegerField(default=0, verbose_name='اعتبار حساب')
    has_comment_permission = models.BooleanField(default=True, verbose_name='اجازه ی ارسال نظر')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = UserManager()

    def avatar_url(self):
        try:
            return self.avatar.url
        except ValueError:
            return '/media/defaults/UserAvatarDefault.jpg'

    def add_credit(self, amount):
        self.balance += amount
        self.save()

    def buy_by_credit(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.save()
            return True
        return False

