from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

"""
urlpatterns = [
    path('profile/<slug:username>/',
         views.UserProfileDetailView.as_view(), name='profile'),
    path('profile/edit_profile/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path('registration/', views.RegistrationCreateView.as_view(), name='registration'),
    
    path('login/', views.LoginView.as_view(), name='login'),
    # Логаут.
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Изменение пароля.
    path('password_change/', views.PasswordChangeView.as_view(),
         name='password_change'),
    # Сообщение об успешном изменении пароля.
    path('password_change/done/', views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # Восстановление пароля.
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # Сообщение об отправке ссылки для восстановления пароля.
    path('password_reset/done/', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    # Вход по ссылке для восстановления пароля.
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # Сообщение об успешном восстановлении пароля.
    path('reset/done/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
"""

