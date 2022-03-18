from django import forms
from .models import ArticleComment, ProductComment

_placeholders = {
    'sender_fullname': 'نام و نام خانوادگی',
    'text': 'متن دیدگاه'
}


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ('sender_fullname', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': _placeholders[field_name]})


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('sender_fullname', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': _placeholders[field_name]})