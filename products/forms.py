from django import forms
from .models import ProductSpecificationValue, Category


class ProductSpecificationValueForm(forms.ModelForm):
    class Meta:
        model = ProductSpecificationValue
        fields = ('specification', 'value')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.instance, 'product'):
            self.fields['specification'].queryset = self.instance.product.category.get_specs()
            if self.instance.specification.values.count():
                self.fields['value'] = forms.ChoiceField(
                    choices=tuple((v.value, v.value) for v in self.instance.specification.values.all()))


class ProductSearchForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'input-select', 'placeholder': 'دسته بندی'}),
        empty_label='همه گروه ها'

    )
    product_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': "input", 'placeholder': "عنوان کالا را وارد کنید ..."})
    )
