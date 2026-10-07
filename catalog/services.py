from django.core.cache import cache

from .models import Product

CACHE_TIMEOUT = 300


def get_products_by_category(category_id: int) -> list[Product]:
    """Возвращает все продукты указанной категории с использованием кеша."""

    cache_key = f"category_{category_id}"

    products = cache.get(cache_key)

    if products is not None:
        return products

    products = list(Product.objects.filter(category_id=category_id))
    cache.set(cache_key, products, CACHE_TIMEOUT)

    return products
