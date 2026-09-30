from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
    )
    published = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию товара"),
        ]

    def __str__(self) -> str:
        return str(self.name)
