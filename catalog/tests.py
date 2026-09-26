from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class ProductAccessTest(TestCase):
    """Тестирует доступ к страницам товаров."""

    def setUp(self) -> None:
        """Создает тестовые данные."""

        self.category = Category.objects.create(
            name="Тестовая категория",
            description="Тестовое описание категории.",
        )

        self.product = Product.objects.create(
            name="Тестовый товар",
            description="Тестовое описание товара.",
            category=self.category,
            price="100.00",
        )

    def test_product_list_is_public(self) -> None:
        """Проверяет доступность списка товаров без авторизации."""

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_requires_login(self) -> None:
        """Проверяет защиту страницы товара."""

        response = self.client.get(reverse("product_detail", kwargs={"pk": self.product.pk}))

        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('product_detail', kwargs={'pk': self.product.pk})}",
        )

    def test_product_create_requires_login(self) -> None:
        """Проверяет защиту создания товара."""

        response = self.client.get(reverse("product_create"))

        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('product_create')}",
        )

    def test_product_update_requires_login(self) -> None:
        """Проверяет защиту редактирования товара."""

        response = self.client.get(reverse("product_update", kwargs={"pk": self.product.pk}))

        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('product_update', kwargs={'pk': self.product.pk})}",
        )

    def test_product_delete_requires_login(self) -> None:
        """Проверяет защиту удаления товара."""

        response = self.client.get(reverse("product_delete", kwargs={"pk": self.product.pk}))

        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('product_delete', kwargs={'pk': self.product.pk})}",
        )
