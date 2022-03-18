from captcha.fields import ReCaptchaField, ReCaptchaV3, ReCaptchaV2Checkbox
from django import forms


class BaseCaptchaV3Form(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV3(api_params={'hl': 'fa'}))


class BaseCaptchaV2Form(forms.Form):
    captcha = ReCaptchaField(
        label='من ربات نیستم',
        widget=ReCaptchaV2Checkbox(api_params={'hl': 'fa'}),
        error_messages={'required': 'لطفا تیک من ریات نیستم را بزنید'}
    )
