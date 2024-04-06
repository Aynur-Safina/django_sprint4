from django.urls import path

from . import views

app_name = 'blog'

#  Я исправила маршруты согласно замечанию.
# Все работает и прекрасно рендерится.
# Но pytest не пропускает c ошибкой:
# "AssertionError: Убедитесь, что опубликованный пост
# с опубликованной категорией и датой публикации
# в прошлом отображается на странице публикации."

urlpatterns = [
    path('', views.PostsHomepageView.as_view(), name='index'),
    path('edit_profile/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'
         ),

    path('profile/<str:username>/',
         views.UserProfileDetailView.as_view(),
         name='profile'
         ),

    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),

    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'
         ),

    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'
         ),

    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'
         ),


    path('posts/<int:post_id>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'
         ),

    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),

    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),

    path(
        'category/<str:category_slug>/',
        views.CategoryDetailView.as_view(),
        name='category_posts'
    ),
]


"""
Вариант маршрутов согласно замечанию.

posts_urls = [
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'
         ),

    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'
         ),

    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'
         ),

    path('posts/<int:post_id>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'
         ),

    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),

    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    )
]

urlpatterns = [
    path('', views.PostsHomepageView.as_view(), name='index'),
    path('posts/', include(posts_urls)),
    path('edit_profile/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'
         ),
    path('profile/<str:username>/',
         views.UserProfileDetailView.as_view(),
         name='profile'
         ),
    path(
        'category/<str:category_slug>/',
        views.CategoryDetailView.as_view(),
        name='category_posts'
    ),
]

"""
