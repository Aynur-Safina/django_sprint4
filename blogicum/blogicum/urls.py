from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import RegistrationCreateView


urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', RegistrationCreateView.as_view(), name='registration'),
    # path('accounts/profile/', UserProfileDetailView.as_view(), name='profile'),
    #
    #


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found'

handler500 = 'core.views.internal_server_error'
