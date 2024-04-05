from blogicum.const import PUBL_COUNT
from core.utils import get_page_obj
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm
from .mixins import (BaseQuerysetMixin, CommentBaseMixin, OnlyAuthorMixin,
                     PostBaseMixin, PostObjectMixin, UrlPostDetailMixin,
                     UrlProfileMixin, UserBaseMixin)
from .models import Category, Post, User


class PostsHomepageView(BaseQuerysetMixin, ListView):
    """Главная страница."""

    template_name = 'blog/index.html'
    paginate_by = PUBL_COUNT


class UserProfileDetailView(UserBaseMixin, DetailView):
    """Страница пользователя(Профиль)."""

    template_name = 'blog/profile.html'

    def get_object(self, **kwarg):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        if self.request.user == user:
            posts = Post.objects.filter(
                author=user,
            )
        else:
            posts = BaseQuerysetMixin.get_queryset(
                self
            ).filter(
                author=user
            )

        context['page_obj'] = get_page_obj(self.request, posts)
        context['profile'] = user
        return context


class ProfileUpdateView(
    UserBaseMixin,
    UrlProfileMixin,
    UpdateView
):
    """Cтраница для редактирования профиля пользователя."""

    fields = (
        'first_name',
        'last_name',
        'username',
        'email',
    )
    template_name = 'blog/user.html'

    # Без этого метода pytest падает с ошибкой 
    # " AttributeError: Generic detail view ProfileUpdateView must be called with either an object pk or a slug in the URLconf." 
    
    def get_object(self, queryset=None):
        return get_object_or_404(
            User,
            username=self.request.user
        )

    def handle_no_permission(self):
        object = self.get_object()
        if object.username != self.request.user:
            raise Http404


class PostDetailView(LoginRequiredMixin, PostObjectMixin, DetailView):
    """Страница отдельной публикации."""

    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            if not post.is_published:
                raise Http404
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.prefetch_related('author')
        )
        return context


class PostCreateView(
    LoginRequiredMixin,
    PostBaseMixin,
    UrlProfileMixin,
    CreateView
):
    """Создание публикации"""

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    OnlyAuthorMixin,
    PostObjectMixin,
    UrlPostDetailMixin,
    UpdateView
):

    pass


class PostDeleteView(
    OnlyAuthorMixin,
    PostObjectMixin,
    UrlProfileMixin,
    DeleteView
):
    """Удаление публикации"""


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


class CategoryDetailView(DetailView):
    """Страница постов, принадлежащих одной категории."""

    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    slug_field = 'slug'

    def get_queryset(self):
        return Category.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        category_id = category.id
        posts = BaseQuerysetMixin.get_queryset(self).filter(
            category=category_id)
        context['page_obj'] = get_page_obj(self.request, posts)
        context['category'] = category
        return context
