from django.db import models
from django.utils import timezone


class PublishedModel(models.Model):
    """Базовая (абстрактная) модель;
    включает общие для всех моедлей атрибуты
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


"""
class PublishedQuerySet(models.QuerySet):
    #Кастомный кверисет, который содержит
    общие для всех моедлей параметры отображения постов на страницах.
    

    def apply_select_related(self):
        return self.select_related(
            'author', 'location', 'category'
        )

    def filter_published(self):
        return self.filter(
            pub_date__lt=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    def base_queryset(self):
        # Mетод-шорткат для применения обоих методов за один
        return self.apply_select_related().filter_published()
"""
