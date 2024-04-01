from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment
from users.forms import MyUserCreationForm


User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин , который предоставляет доступ к редактированию и удалению объектов только авторам — пользователям, создавшим эти объекты."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostsHomepageView(ListView):
    """Главная страница."""
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.prefetch_related(
            'author', 'location', 'category'
        ).filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True,
        ).annotate(comment_count=Count('comments')).all()


class UserProfileDetailView(DetailView):
    """Страница пользователя(Профиль)"""

    model = User
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        posts = Post.objects.filter(author=user)
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['profile'] = user
        return context


class ProfileUpdateView(OnlyAuthorMixin, UpdateView):
    """Cтраница для редактирования профиля пользователя"""

    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'
    form_class = MyUserCreationForm
    exclude = ('username',)
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            User.objects.all(),
            username=self.request.user.username
        )

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user})


class PostDetailView(DetailView):
    """Страница отдельной публикации."""

    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.select_related(
                'author', 'location', 'category'
            ).filter(
                pub_date__lt=timezone.now(),
                is_published=True,
                category__is_published=True,
            ),
            pk=self.kwargs['post_id']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.prefetch_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание публикации"""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user})


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    """Редактирование публикации"""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.all(),
            pk=self.kwargs['post_id'],
        )

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user})


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Удаление публикации"""

    model = Post
    template_name = 'blog/create.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post, pk=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария"""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:index')


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    """Редактирование комментария"""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment.objects.filter(post=self.kwargs['post_id']), pk=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    """Удаление комментария"""

    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment.objects.filter(post=self.kwargs['post_id']), pk=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CategoryListView(DetailView):
    """Страница постов, принадлежащих одной категории."""

    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        category_id = category.id
        posts = Post.objects.filter(pub_date__lt=timezone.now(),
                                    is_published=True,
                                    category__is_published=True,
                                    category=category_id)
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['category'] = category
        return context
