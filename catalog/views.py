from typing import cast

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    """Отображает список товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 3
    ordering = ("id",)


class ContactsTemplateView(TemplateView):
    """Отображает страницу контактов."""

    template_name = "catalog/contacts.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Отображает подробную информацию о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создает новый товар."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self) -> str:
        """Возвращает URL созданного товара."""

        return cast(
            str,
            reverse(
                "product_detail",
                kwargs={"pk": self.object.pk},
            ),
        )


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирует товар."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self) -> str:
        """Возвращает URL отредактированного товара."""

        return cast(
            str,
            reverse(
                "product_detail",
                kwargs={"pk": self.object.pk},
            ),
        )


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет товар."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"

    def get_success_url(self) -> str:
        """Возвращает URL главной страницы."""

        return cast(str, reverse("home"))
