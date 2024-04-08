from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blogicum.const import PUBL_COUNT

from .forms import CommentForm
from .mixins import (BaseQuerysetMixin, CommentBaseMixin, OnlyAuthorMixin,
                     PostBaseMixin, PostObjectMixin, UrlPostDetailMixin,
                     UrlProfileMixin)
from .models import Category, Post, User


class PostsHomepageView(BaseQuerysetMixin, ListView):
    """Главная страница."""

    template_name = 'blog/index.html'
    paginate_by = PUBL_COUNT


class UserProfileDetailView(BaseQuerysetMixin, ListView):
    """Страница пользователя(Профиль)."""

    template_name = 'blog/profile.html'
    paginate_by = PUBL_COUNT

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        profile = self.get_object()
        if self.request.user == profile:
            return (
                Post.objects.select_related(
                    'author'
                ).filter(
                    author=profile,
                ).order_by(
                    '-pub_date'
                ).annotate(
                    comment_count=Count('comments')
                ).all()
            )
        else:
            return BaseQuerysetMixin.get_queryset(
                self
            ).filter(
                author=profile
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UrlProfileMixin, UpdateView):
    """Cтраница для редактирования профиля пользователя."""

    model = User
    fields = (
        'first_name',
        'last_name',
        'username',
        'email',
    )
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user


class PostDetailView(PostBaseMixin, DetailView):
    """Страница отдельной публикации."""

    template_name = 'blog/detail.html'

    def get_object(self):
        self.object = get_object_or_404(
            Post, pk=self.kwargs['post_id']
        )
        if self.object.author != self.request.user:
            return get_object_or_404(
                Post.objects.filter(
                    pub_date__lt=timezone.now(),
                    is_published=True,
                    category__is_published=True,
                ),
                pk=self.kwargs['post_id'],
            )
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostCreateView(
    LoginRequiredMixin,
    PostBaseMixin,
    UrlProfileMixin,
    CreateView
):
    """Создание публикации."""

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    OnlyAuthorMixin,
    PostBaseMixin,
    UrlPostDetailMixin,
    UpdateView
):
    """Редактирование публикации."""

    pass


class PostDeleteView(
    OnlyAuthorMixin,
    PostObjectMixin,
    UrlProfileMixin,
    DeleteView
):
    """Удаление публикации"""

    def get_context_data(self, **kwargs):
        # В шаблон передаем через context форму для удаления
        # и объект для удаления.
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.object)
        context['form'] = form
        return context


class CommentCreateView(
    LoginRequiredMixin,
    CommentBaseMixin,
    CreateView
):
    """Создание комментария"""

    def form_valid(self, form):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)


class CommentUpdateView(
    OnlyAuthorMixin,
    CommentBaseMixin,
    UpdateView
):
    """Редактирование комментария"""

    pass


class CommentDeleteView(OnlyAuthorMixin, CommentBaseMixin, DeleteView):
    """Удаление комментария"""

    pass


class CategoryDetailView(ListView):
    """Страница постов, принадлежащих одной категории."""

    template_name = 'blog/category.html'
    paginate_by = PUBL_COUNT

    def get_object(self):
        return get_object_or_404(
            Category.objects.filter(is_published=True),
            slug=self.kwargs['category_slug']
        )

    def get_queryset(self):
        category = self.get_object()
        return BaseQuerysetMixin.get_queryset(self).filter(
            category=category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context
