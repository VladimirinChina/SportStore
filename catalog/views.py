from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    """Отображает список товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 3


class ContactsTemplateView(TemplateView):
    """Отображает страницу контактов."""

    template_name = "catalog/contacts.html"


class ProductDetailView(DetailView):
    """Отображает подробную информацию о товаре."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Создает новый товар."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self) -> str:
        """Возвращает URL созданного товара."""

        return reverse(
            "product_detail",
            kwargs={"pk": self.object.pk},
        )
