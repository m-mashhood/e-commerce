from django import forms
from django.forms.widgets import FileInput, HiddenInput
from django.utils.safestring import mark_safe

from products.models import Product


class ImagePreviewWidget(FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<br><br><img src="{value.url}" width="300px" height="300px"/>')
        return f'{input_html}{img_html}'


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'name',
            'category',
            'unit',
            'picture',
            'description',
            'in_stock',
            'latest_price',
            'picture',
        )

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.picture is not None:
            self.fields['picture'].widget = ImagePreviewWidget()
        else:
            self.fields['picture'].widget = FileInput()