from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для добавления нового товара."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "price", "category"]
