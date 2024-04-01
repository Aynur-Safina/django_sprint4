from django.db import models
from django.contrib.auth import get_user_model
from blogicum.const import MAXLENGTH, VISIBLE_LENGTH

from core.models import PublishedModel

User = get_user_model()


class Post(PublishedModel):
    """Модель публикации."""

    title = models.CharField(
        max_length=MAXLENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        null=True,
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        null=True,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем —'
            ' можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )

    image = models.ImageField(
        'Изображение',
        upload_to='posts_images',
        blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

   # def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        # return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title[:VISIBLE_LENGTH]


class Category(PublishedModel):
    """Модель категории публикации."""

    title = models.CharField(
        max_length=MAXLENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:VISIBLE_LENGTH]


class Location(PublishedModel):
    """Модель места публикации."""

    name = models.CharField(
        max_length=MAXLENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:VISIBLE_LENGTH]


class Comment(models.Model):
    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
