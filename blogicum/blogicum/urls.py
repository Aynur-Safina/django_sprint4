from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from users.views import RegistrationCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        RegistrationCreateView.as_view(),
        name='registration'
    ),
    path('', include('blog.urls', namespace='blog')),
]
# Медиа от пользователя
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]

handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.internal_server_error'
