from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.constants import RoleChoices


class User(AbstractUser):
    role = models.CharField(
        verbose_name="Роль пользователя",
        max_length=50,
        null=True,
        blank=True,
        choices=RoleChoices.choices,
    )
    email = models.EmailField(verbose_name="Почта", blank=True)
    phone = PhoneNumberField(verbose_name="Телефон", max_length=13, blank=True)
    photo = models.ImageField(upload_to="u/u/p", verbose_name="Фото пользователя", null=True)

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"

    def __str__(self) -> str:
        return f"Пользователь - {self.username}"
