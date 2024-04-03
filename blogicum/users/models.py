from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class MyUser(AbstractUser):

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('blog:profile', kwargs={'slug': self.slug})
