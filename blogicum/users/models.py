from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# Create your models here.


class MyUser(AbstractUser):

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('blog:profile', kwargs={'slug': self.slug})
