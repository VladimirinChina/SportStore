from decimal import Decimal

from django import forms

from .models import Product


FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    """Форма для добавления нового товара."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "price", "category"]

    def __init__(self, *args, **kwargs) -> None:
        """Добавляет CSS-классы полям формы."""

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


    def clean_name(self) -> str:
        """Проверяет название товара на наличие запрещенных слов."""

        name = self.cleaned_data["name"]

        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(
                    f"Название содержит запрещенное слово: {word}."
                )

        return name


    def clean_description(self) -> str:
        """Проверяет описание товара на наличие запрещенных слов."""

        description = self.cleaned_data["description"]

        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(
                    f"Описание содержит запрещенное слово: {word}."
                )

        return description

    def clean_price(self) -> Decimal:
        """Проверяет, что цена товара не является отрицательной."""

        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError(
                "Цена товара не может быть отрицательной."
            )

        return price