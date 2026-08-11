from typing import Any

from django.core.management import BaseCommand, call_command

from catalog.models import Category, Product


class Command(BaseCommand):
    """Загружает тестовые данные из фикстур."""

    help = "Удаляет существующие категории и продукты и загружает тестовые данные"

    def handle(self, *args: Any, **options: Any) -> None:
        """Удаляет существующие данные и загружает фикстуры."""

        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "categories.json")
        call_command("loaddata", "products.json")

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены."))
