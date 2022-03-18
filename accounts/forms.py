from captcha.fields import ReCaptchaField, ReCaptchaV2Checkbox
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, _unicode_ci_compare, \
    SetPasswordForm, PasswordChangeForm
from django.contrib.auth import get_user_model, authenticate
from django import forms
from validate_email import validate_email
from utilties.captcha_form import BaseCaptchaV2Form

_User = get_user_model()

placeholders = {
    'full_name': 'نام و نام خانوادگی',
    'username': 'ایمیل',
    'email': 'ایمیل',
    'password1': 'رمز عبور',
    'password': 'رمز عبور',
    'password2': 'تکرار رمز عبور',
    'new_password1': 'رمز عبور جدید',
    'new_password2': 'تکرار رمز عبور جدید',
    'old_password': 'رمز عبور فعلی',
    'address': 'آدرس',
    'phone': 'شماره موبایل',

}


class UserRegistrationForm(UserCreationForm):
    captcha = ReCaptchaField(
        label='من ربات نیستم',
        widget=ReCaptchaV2Checkbox(api_params={'hl': 'fa'}),
        error_messages={'required': 'لطفا تیک من ریات نیستم را بزنید'}
    )
    rules = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ('full_name', 'email', 'password1', 'password2', 'phone', 'address'):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = placeholders[field_name]

    class Meta:
        model = _User
        fields = ('full_name', 'email', 'password1', 'password2')

    def clean_rules(self):
        rules = self.cleaned_data['rules']
        if rules:
            return rules
        raise forms.ValidationError('شما باید قوانین سایت را بپذیرید')


class ResendActivationForm(BaseCaptchaV2Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))

    def clean_email(self):
        initial_email = self.cleaned_data.get('email')
        if validate_email(initial_email):
            return initial_email
        raise forms.ValidationError('این ایمیل معتبر نیست')

    def clean(self):
        email = self.cleaned_data.get('email')
        try:
            user = _User.objects.get(email=email)
        except _User.DoesNotExist:
            raise forms.ValidationError('شما ثبت نام نکرده اید')
        else:
            if user.is_active:
                raise forms.ValidationError('حساب کاربری شما قبلا فعال شده است')
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    captcha = ReCaptchaField(
        label='من ربات نیستم',
        widget=ReCaptchaV2Checkbox(api_params={'hl': 'fa'}),
        error_messages={'required': 'لطفا تیک من ربات نیستم را بزنید'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != 'captcha':
                self.fields[field_name].widget.attrs['class'] = 'form-control'
                self.fields[field_name].widget.attrs['placeholder'] = placeholders[field_name]

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                try:
                    user_temp = _User.objects.get(email=email)
                except _User.DoesNotExist:
                    user_temp = None

                if user_temp is not None and user_temp.check_password(password):
                    self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
        return self.cleaned_data


class PWResetForm(PasswordResetForm):
    captcha = ReCaptchaField(
        label='من ربات نیستم',
        widget=ReCaptchaV2Checkbox(api_params={'hl': 'fa'}),
        error_messages={'required': 'لطفا تیک من ریات نیستم را بزنید'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ایمیل'})

    def get_users(self, email):
        email_field_name = _User.get_email_field_name()
        active_users = _User.objects.filter(**{
            '%s__iexact' % email_field_name: email,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
               _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            _User.objects.get(email=cleaned_data['email'])
        except _User.DoesNotExist:
            raise forms.ValidationError('شما ثبت نام نکرده اید')
        return cleaned_data


class PWResetConfirmForm(SetPasswordForm):
    captcha = ReCaptchaField(
        label='من ربات نیستم',
        widget=ReCaptchaV2Checkbox(api_params={'hl': 'fa'}),
        error_messages={'required': 'لطفا تیک من ریات نیستم را بزنید'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'captcha':
                field.widget.attrs.update({'class': 'form-control', 'placeholder': placeholders[field_name]})


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = _User
        fields = ('avatar', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'avatar':
                field.widget.attrs.update({'class': 'form-control', 'placeholder': placeholders[field_name]})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class PWChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': placeholders[field_name]})


class AddBalanceForm(forms.Form):
    amount = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'مبلغ مورد نظر'}))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        try:
            to_int = int(amount)
        except ValueError:
            raise forms.ValidationError('مبلغ وارد شده یک عدد صحیح نیست')
        else:
            if to_int >= 1000:
                return amount
            raise forms.ValidationError('حداقل مبلغ قابل پرداخت 1000 تومان می باشد.')
