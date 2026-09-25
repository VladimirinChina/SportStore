from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = None
    email = models.EmailField(unique=True)

    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )
    country = models.CharField(
        max_length=100,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    def __str__(self) -> str:
        return str(self.email)
