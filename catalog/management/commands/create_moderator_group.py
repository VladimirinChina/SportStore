from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db.models import QuerySet


class Command(BaseCommand):
    """Создает группу модераторов продуктов и назначает ей права."""

    help = "Создает группу «Модератор продуктов» с правами модерации товаров."

    def handle(self, *args: Any, **options: Any) -> None:
        """Создает группу и назначает ей необходимые permissions."""

        group, created = Group.objects.get_or_create(
            name="Модератор продуктов",
        )

        permissions: QuerySet[Permission] = Permission.objects.filter(
            content_type__app_label="catalog",
            codename__in=[
                "can_unpublish_product",
                "delete_product",
            ],
        )

        group.permissions.set(permissions)

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Группа «Модератор продуктов» создана и права назначены.",
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Группа «Модератор продуктов» уже существует. Права обновлены.",
                )
            )
