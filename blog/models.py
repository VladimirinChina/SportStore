from django.db import models


class Blog(models.Model):
    """Модель блоговой записи."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    preview = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "блоговая запись"
        verbose_name_plural = "блоговые записи"

    def __str__(self) -> str:
        return str(self.title)
