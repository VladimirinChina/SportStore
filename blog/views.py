from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Blog


class BlogListView(ListView):
    """Отображает список опубликованных блоговых записей."""

    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = "blogs"

    def get_queryset(self):
        """Возвращает только опубликованные блоговые записи."""

        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Отображает подробную информацию о блоговой записи."""

    model = Blog
    template_name = "blog/blog_detail.html"
    context_object_name = "blog"

    def get_object(self, queryset=None):
        """Возвращает запись и увеличивает счетчик просмотров."""

        blog = super().get_object(queryset)
        blog.views_count += 1
        blog.save()

        return blog


class BlogCreateView(CreateView):
    """Создает новую блоговую запись."""

    model = Blog
    fields = [
        "title",
        "content",
        "preview",
        "is_published",
    ]
    template_name = "blog/blog_form.html"

    def get_success_url(self) -> str:
        """Возвращает URL созданной записи."""

        return reverse(
            "blog_detail",
            kwargs={"pk": self.object.pk},
        )


class BlogUpdateView(UpdateView):
    """Редактирует блоговую запись."""

    model = Blog
    fields = [
        "title",
        "content",
        "preview",
        "is_published",
    ]
    template_name = "blog/blog_form.html"

    def get_success_url(self) -> str:
        """Возвращает URL отредактированной записи."""

        return reverse(
            "blog_detail",
            kwargs={"pk": self.object.pk},
        )


class BlogDeleteView(DeleteView):
    """Удаляет блоговую запись."""

    model = Blog
    template_name = "blog/blog_confirm_delete.html"

    def get_success_url(self) -> str:
        """Возвращает URL списка блоговых записей."""

        return reverse("blog_list")
