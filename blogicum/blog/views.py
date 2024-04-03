from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment


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
    для создания, редактирования и удаления публикации."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class PostObjectMixin(PostBaseMixin):
    """Миксин, дополнящий PostBaseMixin. 
    Для редактирования и удаления публикации."""

    def get_object(self):
        return get_object_or_404(
            Post, pk=self.kwargs['post_id'])


class BaseQueryset():
    """Миксин содержит основные фильтры для постов и комментов"""
    
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
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user})


class UrlPostDetailMixin():
    """Миксин переадресует на страницу Post_Detail."""
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentBaseMixin(UrlPostDetailMixin):
    """Миксин с базовыми атрибутами комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment.objects.filter(post=self.kwargs['post_id']), pk=self.kwargs['comment_id'])


def get_page_obj(request,  paginated_obj):
    """Пагинация по 10 публикаций на странице."""
    
    paginator = Paginator(paginated_obj, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


class PostsHomepageView(BaseQueryset, ListView):
    """Главная страница."""

    template_name = 'blog/index.html'
    paginate_by = 10 

    def get_queryset(self):
        # Применеям get_queryset родительского класса(BaseQueryset)+дополнительный фильтр.
        return super().get_queryset().annotate(
            comment_count=Count('comments')
            ).all()


class UserProfileDetailView(UserBaseMixin, DetailView):
    """Страница пользователя(Профиль)"""

    template_name = 'blog/profile.html'

    def get_object(self, **kwarg):
        return get_object_or_404(User, username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        if self.request.user == user:
            posts = Post.objects.filter(
                author=user,
                ).order_by(
                '-pub_date'
                ).annotate(
                comment_count=Count('comments')
                ).all()
            
        else:
            posts = BaseQueryset.get_queryset(
                self
                ).filter(
                author=user
                ).order_by(
                '-pub_date'
                ).annotate(
                comment_count=Count('comments')
                ).all()
            
        context['page_obj'] = get_page_obj(self.request, posts)
        context['profile'] = user
        return context
    

class ProfileUpdateView(
    UserBaseMixin,
    UrlProfileMixin,
    UpdateView
    ):
    """Cтраница для редактирования профиля пользователя"""
    fields=(
        'first_name',
        'last_name',
        'username',
        'email',
        )
    template_name = 'blog/user.html'

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
    CreateView):
    """Создание комментария"""

    def form_valid(self, form):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)


class CommentUpdateView(OnlyAuthorMixin, CommentBaseMixin, UrlPostDetailMixin, UpdateView):
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
        posts = BaseQueryset.get_queryset(self).filter(
            category=category_id)
        context['page_obj'] = get_page_obj(self.request, posts)
        context['category'] = category
        return context
