from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Post, Category, Location


# Удалила дефолтную модель *Group* из админки
admin.site.unregister(Group)

# Кастомизация админ панели ()
admin.site.site_header = "Админ-панель 'Блогикум'"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в админку, друг!"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'pub_date',
        'is_published',
    )
    list_editable = (
        'is_published',
        'category',
    )
    search_fields = (
        'title',
        'author',
        'category',
    )
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
    )
    list_editable = (
        'is_published',
        'slug',
    )
    search_fields = (
        'title',
        'slug',
    )
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'name',
    )
    list_filter = ('is_published',)
    list_display_links = ('name',)


admin.site.empty_value_display = 'Не задано'
