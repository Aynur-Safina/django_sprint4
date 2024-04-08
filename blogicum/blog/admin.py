from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post

# Удалила дефолтную модель *Group* из админки.
admin.site.unregister(Group)

# Кастомизация админ-панели.
admin.site.site_header = "Админ-панель 'Блогикум'"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в админку, друг!"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Группировка полей при добавлении новой публикации через админ-панель
    fieldsets = (
        ('Инфо', {
            'fields': ('title', 'author', 'pub_date',),
            'description': 'Общая информация'
        }),
        ('Категория', {
            'fields': ('category',),
        }),
        ('Иллюстрация', {
            'fields': ('get_image_tag',)
        })
    )

    list_display = (
        'title',
        'author',
        'pub_date',
        'category',
        'is_published',
        'get_image_tag',
    )

    # Поля, которые можно только читать(не редактировать)
    readonly_fields = ('get_image_tag',)

    search_fields = (
        'title',
        'author',
        'category',
    )
    list_filter = ('is_published',
                   'category')

    @admin.display(
        description='Иллюстрация к посту',
    )
    def get_image_tag(self, obj):
        """Метод выводит миниатюру иллюстрации к посту в
        админ-панель(без него будет только ссылка на иллюстрацию).
        """
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=50>')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Информация', {
            'fields': ('title', 'description',),

        }),
        ('Статус категории', {
            'fields': ('slug', 'is_published',)
        }),
    )
    search_fields = (
        'title',
        'slug',
    )
    list_filter = ('is_published',)
    list_display = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    filelds = ['name',
               'is_published', ]
    list_display = (
        'name',
        'is_published',
    )
    search_fields = (
        'name',
    )
    list_filter = ('is_published',)
    list_display = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'text',
        'author',
        'created_at',
    )
    search_fields = (
        'author',
        'post',
        'created_at',
    )
    list_display_links = ('text',)


admin.site.empty_value_display = 'Не задано'
