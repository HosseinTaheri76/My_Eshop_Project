from captcha.fields import ReCaptchaField, ReCaptchaV2Checkbox
from django import forms
from .models import UserMessage

placeholders = {
    'full_name': 'نام و نام خانوادگی',
    'title': 'موضوع پیام',
    'phone': 'شماره موبایل',
    'email': 'ایمیل',
    'question_text': 'متن پیام'
}


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ('full_name', 'title', 'phone', 'email', 'question_text')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        if not request.user.is_authenticated:
            self.fields['captcha'] = ReCaptchaField(
                label='من ربات نیستم',
                widget=ReCaptchaV2Checkbox(api_params={'hl': 'fa'}),
                error_messages={'required': 'لطفا تیک من ریات نیستم را بزنید'}
            )
        for field_name, field in self.fields.items():
            if field_name != 'captcha':
                field.widget.attrs.update({'class': 'form-control', 'placeholder': placeholders[field_name]})
                if field_name == 'question_text':
                    field.widget.attrs.update({'rows': 7})
