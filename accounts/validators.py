from django.core.exceptions import ValidationError
import re


def validate_phone(value):
    pattern = re.compile(r'^(0098|\+98|0)9\d{9}$')
    if pattern.match(value):
        return value
    raise ValidationError('شماره ی وارد شده شماره ی تلفن همراه معتبری نیست.')
