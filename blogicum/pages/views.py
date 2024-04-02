from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """Страница 'О проекте'."""

    template_name: str = 'pages/about.html'


class Rules(TemplateView):
    """Страница 'Правила'."""

    template_name: str = 'pages/rules.html'


def page_not_found(request, exception):
    """Кастомная страница для ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Кастомная страница для ошибки 403 CSRF."""
    return render(request, 'pages/403csrf.html', status=403)


def internal_server_error(request):
    """Кастомная страница для ошибки 500."""
    return render(request, 'pages/500.html', status=500)
