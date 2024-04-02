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
