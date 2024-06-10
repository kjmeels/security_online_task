import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from ..constants import RoleChoices
from ..models import User


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda x: f"user_{x}")
    role = fuzzy.FuzzyChoice(choices=RoleChoices.values)
    email = factory.Sequence(lambda x: f"email{x}@mail.ru")
    phone = "+375291234567"
    photo = factory.django.ImageField(filename="test.png")

    class Meta:
        model = User
