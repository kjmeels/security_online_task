import factory
from factory.django import DjangoModelFactory

from users.tests.factories import UserFactory
from ..constants import StatusChoices
from ..models import Task


class TaskFactory(DjangoModelFactory):
    status = StatusChoices.AWAITS
    customer = factory.SubFactory(UserFactory)
    employee = factory.SubFactory(UserFactory)
    ended_at = None
    report = ""
    task_detail = factory.Faker("sentence")

    class Meta:
        model = Task
