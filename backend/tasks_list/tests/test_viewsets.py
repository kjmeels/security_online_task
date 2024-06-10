from functools import partial

from pytest import mark
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.constants import RoleChoices
from users.tests.factories import UserFactory
from .factories import TaskFactory
from ..constants import StatusChoices
from ..models import Task


@mark.django_db
class TestTaskViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("tasks_list-list")
        self.update_url = partial(reverse, "tasks_list-detail")

    def test_add_task(self):
        user = UserFactory(role=RoleChoices.CUSTOMER)

        self.client.force_authenticate(user=user)

        payload = {
            "task_detail": "New task",
        }

        with self.assertNumQueries(1):
            res = self.client.post(self.list_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().customer, user)

    def test_list(self):
        user = UserFactory(role=RoleChoices.CUSTOMER)
        tasks = [TaskFactory(customer=user) for _ in range(5)]
        other_tasks = [TaskFactory() for _ in range(5)]

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(1):
            res = self.client.get(self.list_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(tasks))

    def test_update_status(self):
        user = UserFactory(role=RoleChoices.STAFF)
        self.client.force_authenticate(user=user)

        task = TaskFactory(employee=user)

        payload = {
            "status": StatusChoices.IN_PROGRESS.value,
            "task_detail": "task #",
            "report": "",
        }

        with self.assertNumQueries(2):
            res = self.client.put(self.update_url(kwargs={"pk": task.id}), data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, StatusChoices.IN_PROGRESS)

    def test_update_report(self):
        user = UserFactory(role=RoleChoices.STAFF)
        self.client.force_authenticate(user=user)

        task = TaskFactory(employee=user)

        payload = {
            "status": StatusChoices.COMPLETED.value,
            "task_detail": "task #",
            "report": "development task completed",
        }

        with self.assertNumQueries(2):
            res = self.client.put(self.update_url(kwargs={"pk": task.id}), data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.first().status, StatusChoices.COMPLETED)
        self.assertIsNotNone(Task.objects.first().report)

    def test_update_error(self):
        user = UserFactory(role=RoleChoices.STAFF)
        self.client.force_authenticate(user=user)

        task = TaskFactory(employee=user)

        payload = {
            "status": StatusChoices.COMPLETED.value,
            "task_detail": "task #",
            "report": "",
        }

        with self.assertNumQueries(1):
            res = self.client.put(self.update_url(kwargs={"pk": task.id}), data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        task.refresh_from_db()
        self.assertNotEqual(task.status, StatusChoices.COMPLETED)
