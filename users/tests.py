from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserRegistrationTest(TestCase):
    """Тестирует регистрацию пользователя."""

    def test_user_registration(self) -> None:
        """Проверяет создание пользователя через форму регистрации."""

        response = self.client.post(
            reverse("users:register"),
            {
                "email": "test@example.com",
                "password1": "TestPassword123!",
                "password2": "TestPassword123!",
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(email="test@example.com").exists())


class UserLoginTest(TestCase):
    """Тестирует авторизацию пользователя."""

    def setUp(self) -> None:
        """Создает пользователя для тестов."""

        self.password = "TestPassword123!"

        self.user = User.objects.create_user(
            email="test@example.com",
            password=self.password,
        )

    def test_user_login(self) -> None:
        """Проверяет вход пользователя по email и паролю."""

        response = self.client.post(
            reverse("users:login"),
            {
                "username": self.user.email,
                "password": self.password,
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class UserProfileTest(TestCase):
    """Тестирует защиту страницы профиля."""

    def test_anonymous_user_cannot_access_profile(self) -> None:
        """Проверяет перенаправление неавторизованного пользователя."""

        response = self.client.get(reverse("users:profile"))

        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('users:profile')}",
        )
