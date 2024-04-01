from django.views.generic import TemplateView


class About(TemplateView):
    """Страница 'О проекте'."""

    template_name: str = 'pages/about.html'


class Rules(TemplateView):
    """Страница 'Правила'."""

    template_name: str = 'pages/rules.html'
