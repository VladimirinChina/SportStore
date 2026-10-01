from typing import Any, cast

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
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

    def form_valid(self, form: ProductForm) -> HttpResponse:
        """Устанавливает текущего пользователя владельцем товара."""

        form.instance.owner = self.request.user

        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Возвращает URL созданного товара."""

        return cast(
            str,
            reverse(
                "product_detail",
                kwargs={"pk": self.object.pk},
            ),
        )


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирует товар."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def test_func(self) -> bool:
        """Проверяет, является ли пользователь владельцем или модератором."""

        product = self.get_object()

        return bool(product.owner == self.request.user or self.request.user.has_perm("catalog.can_unpublish_product"))

    def get_success_url(self) -> str:
        """Возвращает URL отредактированного товара."""

        return cast(
            str,
            reverse(
                "product_detail",
                kwargs={"pk": self.object.pk},
            ),
        )


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаляет товар."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"

    def test_func(self) -> bool:
        """Проверяет, является ли пользователь владельцем или модератором."""

        product = self.get_object()

        return bool(product.owner == self.request.user or self.request.user.has_perm("catalog.delete_product"))

    def get_success_url(self) -> str:
        """Возвращает URL главной страницы."""

        return cast(str, reverse("home"))


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Отменяет публикацию товара."""

    def test_func(self) -> bool:
        """Проверяет право пользователя на отмену публикации."""

        return bool(self.request.user.has_perm("catalog.can_unpublish_product"))

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Отменяет публикацию товара."""

        product = get_object_or_404(Product, pk=kwargs["pk"])
        product.published = False
        product.save(update_fields=["published", "updated_at"])

        return redirect("product_detail", pk=product.pk)
