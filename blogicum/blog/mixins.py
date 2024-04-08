from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import CommentForm, PostForm
from .models import Comment, Post


class OnlyAuthorMixin(UserPassesTestMixin):
    """Класс для ограничения доступа не-авторов.

    Атрибуты:
    __________
    наследуются от UserPassesTestMixin.

    Методы:
    ________
    переопределяет родительские методы:
    - test_func - определяет, является ли текущий пользователь автором объекта
    - handle_no_permission - перенаправляет на другие страницы
    в случае возникновения исключения PermissionDenied.

    """

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        object = self.get_object()
        if not self.request.user.is_authenticated:
            return redirect('login')
        return redirect('blog:post_detail', post_id=object.id, permanent=True)


class PostBaseMixin:
    """Миксин для создания, редактирования и удаления публикации.

    Атрибуты:
    __________
    model - модель класса для публикаций
    form_class - форма для публикаций
    template_name - шаблон HTML
    pk_url_kwarg - переопределение параметра pk
    """

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class PostObjectMixin(PostBaseMixin):
    """Миксин, дополнящий PostBaseMixin."""

    def get_object(self):
        return get_object_or_404(
            Post, pk=self.kwargs['post_id'])


class BaseQuerysetMixin:
    """Миксин содержит основные фильтры для постов и комментов."""

    def get_queryset(self):
        return Post.objects.prefetch_related(
            'author', 'location', 'category'
        ).filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments')
        ).all()


class UrlProfileMixin():
    """Миксин переадресует на страницу Profile."""

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class UrlPostDetailMixin():
    """Миксин переадресует на страницу Post_Detail."""

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentBaseMixin(UrlPostDetailMixin):
    """Миксин с базовыми атрибутами комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment.objects.filter(post=self.kwargs['post_id']),
            pk=self.kwargs['comment_id']
        )
