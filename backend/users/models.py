from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # role =
    # email = models.EmailField(verbose_name="Почта", unique=True)
    # phone = PhoneNumberField()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"
