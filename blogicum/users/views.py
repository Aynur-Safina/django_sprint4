from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth import get_user_model
from .forms import MyUserCreationForm
from blog.models import Post

User = get_user_model


class RegistrationCreateView(CreateView):
    template_name='registration/registration_form.html'
    form_class = MyUserCreationForm
    slug_url_kwarg = 'username'
    success_url = reverse_lazy('blog:index')
    





   
"""
    def get_object(self, queryset=None):
        return get_object_or_404(
            User.objects.all(),
            slug=self.kwargs['username']
        )

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.object})
    """
