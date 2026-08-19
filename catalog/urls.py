from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path(
        "contacts/",
        views.ContactsTemplateView.as_view(),
        name="contacts",
    ),
    path(
        "products/create/",
        views.ProductCreateView.as_view(),
        name="product_create",
    ),
    path(
        "products/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]
