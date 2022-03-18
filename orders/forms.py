from accounts.forms import UserRegistrationForm, placeholders
from django.contrib.auth import get_user_model
from .models import Order
from django import forms


class RegisterOnOrderForm(UserRegistrationForm):
    class Meta:
        model = get_user_model()
        fields = ('full_name', 'email', 'password1', 'password2', 'phone', 'address')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('phone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = placeholders[field_name]
