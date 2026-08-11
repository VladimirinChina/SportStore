from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Отображает главную страницу магазина."""

    return render(request, "catalog/home.html")


def contacts(request: HttpRequest) -> HttpResponse:
    """Отображает страницу контактов."""

    return render(request, "catalog/contacts.html")
