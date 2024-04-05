from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import MyUserCreationForm

User = get_user_model


class RegistrationCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = MyUserCreationForm
    slug_url_kwarg = 'username'
    success_url = reverse_lazy('blog:index')
