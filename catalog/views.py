from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import ProductForm
from .models import Product


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу магазина."""

    products = Product.objects.all()
    paginator = Paginator(products, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "catalog/home.html",
        {"page_obj": page_obj},
    )


def contacts(request: HttpRequest) -> HttpResponse:
    """Отображает страницу контактов."""

    return render(request, "catalog/contacts.html")


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Отображает страницу с подробной информацией о товаре."""

    product = Product.objects.get(pk=pk)

    return render(request, "catalog/product_detail.html", {"product": product})


def product_create(request: HttpRequest) -> HttpResponse:
    """Создает новый товар."""

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "catalog/product_form.html", {"form": form})
