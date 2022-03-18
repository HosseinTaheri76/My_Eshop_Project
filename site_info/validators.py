from django.core.exceptions import ValidationError


def validate_static_phone_number(value):
    value = value.replace('-', '').replace('_', '')
    if value.isdigit() and 2 < len(value) < 12:
        return value
    raise ValidationError('عبارت وارد شده یک شماره تلفن ثابت معتبر نیست')
