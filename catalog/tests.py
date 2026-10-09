from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product
from .services import get_products_by_category

User = get_user_model()


class ProductAccessTest(TestCase):
    """Тестирует доступ к страницам товаров."""

    def setUp(self) -> None:
        """Создает тестовые данные."""

        self.user = User.objects.create_user(
            email="owner@example.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="test-password",
        )

        self.moderator = User.objects.create_user(
            email="moderator@example.com",
            password="test-password",
        )

        self.moderator_group = Group.objects.create(
            name="Модератор продуктов",
        )

        permissions = Permission.objects.filter(
            content_type__app_label="catalog",
            codename__in=[
                "can_unpublish_product",
                "delete_product",
            ],
        )

        self.moderator_group.permissions.set(permissions)
        self.moderator.groups.add(self.moderator_group)

        self.category = Category.objects.create(
            name="Тестовая категория",
            description="Тестовое описание категории.",
        )

        self.product = Product.objects.create(
            name="Тестовый товар",
            description="Тестовое описание товара.",
            category=self.category,
            owner=self.user,
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

    def test_product_owner_is_current_user_on_create(self) -> None:
        """Проверяет автоматическое назначение владельца при создании товара."""

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("product_create"),
            {
                "name": "Новый товар",
                "description": "Описание нового товара.",
                "price": "200.00",
                "category": self.category.pk,
            },
        )

        self.assertRedirects(
            response,
            reverse("product_detail", kwargs={"pk": Product.objects.latest("pk").pk}),
        )

        product = Product.objects.get(name="Новый товар")

        self.assertEqual(product.owner, self.user)

    def test_product_owner_can_update_product(self) -> None:
        """Проверяет, что владелец может редактировать свой товар."""

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("product_update", kwargs={"pk": self.product.pk}),
        )

        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_update_product(self) -> None:
        """Проверяет, что другой пользователь не может редактировать товар."""

        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("product_update", kwargs={"pk": self.product.pk}),
        )

        self.assertEqual(response.status_code, 403)

    def test_product_owner_can_delete_product(self) -> None:
        """Проверяет, что владелец может удалить свой товар."""

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("product_delete", kwargs={"pk": self.product.pk}),
        )

        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_delete_product(self) -> None:
        """Проверяет, что другой пользователь не может удалить товар."""

        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("product_delete", kwargs={"pk": self.product.pk}),
        )

        self.assertEqual(response.status_code, 403)

    def test_moderator_can_update_product(self) -> None:
        """Проверяет, что модератор может редактировать чужой товар."""

        self.client.force_login(self.moderator)

        response = self.client.get(
            reverse("product_update", kwargs={"pk": self.product.pk}),
        )

        self.assertEqual(response.status_code, 200)

    def test_moderator_can_delete_product(self) -> None:
        """Проверяет, что модератор может удалить чужой товар."""

        self.client.force_login(self.moderator)

        response = self.client.get(
            reverse("product_delete", kwargs={"pk": self.product.pk}),
        )

        self.assertEqual(response.status_code, 200)


class ProductUnpublishTest(TestCase):
    """Тестирует отмену публикации товара."""

    def setUp(self) -> None:
        """Создает пользователя, категорию и опубликованный товар."""

        self.user = User.objects.create_user(
            email="user@example.com",
            password="TestPassword123!",
        )

        self.category = Category.objects.create(
            name="Тестовая категория",
            description="Тестовое описание категории.",
        )

        self.product = Product.objects.create(
            name="Опубликованный товар",
            description="Тестовое описание товара.",
            category=self.category,
            price="100.00",
            owner=self.user,
            published=True,
        )

    def test_user_without_permission_cannot_unpublish(self) -> None:
        """Проверяет запрет отмены публикации без права."""

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("product_unpublish", kwargs={"pk": self.product.pk}),
        )

        self.assertEqual(response.status_code, 403)

        self.product.refresh_from_db()
        self.assertTrue(self.product.published)

    def test_user_with_permission_can_unpublish(self) -> None:
        """Проверяет отмену публикации пользователем с правом."""

        permission = Permission.objects.get(
            codename="can_unpublish_product",
        )
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("product_unpublish", kwargs={"pk": self.product.pk}),
        )

        self.assertRedirects(
            response,
            reverse("product_detail", kwargs={"pk": self.product.pk}),
        )

        self.product.refresh_from_db()
        self.assertFalse(self.product.published)


class ProductCategoryCacheTest(TestCase):
    """Тестирует низкоуровневое кеширование товаров категории."""

    def setUp(self) -> None:
        """Создает категорию и товары для тестирования."""

        cache.clear()

        self.user = User.objects.create_user(
            email="cache-owner@example.com",
            password="test-password",
        )

        self.category = Category.objects.create(
            name="Категория для кеша",
            description="Описание категории для тестирования.",
        )

        self.product = Product.objects.create(
            name="Товар для кеша",
            description="Описание товара для тестирования.",
            category=self.category,
            owner=self.user,
            price="150.00",
        )

    def tearDown(self) -> None:
        """Очищает кеш после теста."""

        cache.clear()

    def test_first_call_queries_database_and_caches_products(self) -> None:
        """Первый вызов получает товары из БД и сохраняет их в кеш."""

        with self.assertNumQueries(1):
            products = get_products_by_category(self.category.pk)

        self.assertEqual(products, [self.product])
        self.assertIsInstance(products, list)
        self.assertEqual(
            cache.get(f"category_{self.category.pk}"),
            [self.product],
        )

    def test_second_call_returns_cached_products(self) -> None:
        """Повторный вызов возвращает товары из кеша без запроса к БД."""

        cached_products = [self.product]
        cache.set(f"category_{self.category.pk}", cached_products, 300)

        with patch("catalog.services.Product.objects.filter") as mock_filter:
            products = get_products_by_category(self.category.pk)

        self.assertEqual(products, cached_products)
        mock_filter.assert_not_called()

    def test_cache_timeout_is_300_seconds(self) -> None:
        """Проверяет, что сервис сохраняет кеш на 300 секунд."""

        with patch("catalog.services.cache.set") as mock_cache_set:
            get_products_by_category(self.category.pk)

        mock_cache_set.assert_called_once()
        args, kwargs = mock_cache_set.call_args

        self.assertEqual(args[0], f"category_{self.category.pk}")
        self.assertEqual(args[2], 300)
