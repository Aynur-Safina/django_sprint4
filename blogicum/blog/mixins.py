from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import PostForm, CommentForm
from .models import Post, Comment


User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин, который предоставляет доступ к редактированию
    и удалению объектов только авторам — пользователям,
    создавшим эти объекты.
    """

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        object = self.get_object()
        if not self.request.user.is_authenticated:
            return redirect('login')
        return redirect('blog:post_detail', post_id=object.id, permanent=True)


class PostBaseMixin():
    """Миксин, содержащий основные атрибуты классов
    для создания, редактирования и удаления публикации.
    """

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class PostObjectMixin(PostBaseMixin):
    """Миксин, дополнящий PostBaseMixin.
    Для редактирования и удаления публикации.
    """

    def get_object(self):
        return get_object_or_404(
            Post, pk=self.kwargs['post_id'])


class BaseQuerysetMixin():
    """Миксин содержит основные фильтры для постов и комментов."""

    def get_queryset(self):
        return Post.objects.prefetch_related(
            'author', 'location', 'category'
        ).filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).order_by('-pub_date')


class UserBaseMixin():
    """Миксин с базовыми атрибутами для User."""

    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'
    content_object_name = 'profile'


class UrlProfileMixin():
    """Миксин переадресует на страницу Profile."""

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class UrlPostDetailMixin():
    """Миксин переадресует на страницу Post_Detail."""

    def get_success_url(self):
        return reverse_lazy(
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
