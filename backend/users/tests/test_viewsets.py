from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase

from users.constants import RoleChoices
from users.models import User
from users.tests.factories import UserFactory
from users.utils import generate_image_file


@mark.django_db
class TestUserViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("users-list")
        self.about_me_url: str = reverse("users-about-me")

    def test_list_customer(self):
        user1 = UserFactory(role=RoleChoices.CUSTOMER)
        users = [UserFactory(role=RoleChoices.STAFF) for _ in range(5)]

        self.client.force_authenticate(user=user1)

        with self.assertNumQueries(1):
            res = self.client.get(self.list_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(users))

    def test_about_me_customer(self):
        users = [UserFactory(role=RoleChoices.CUSTOMER) for _ in range(5)]

        self.client.force_authenticate(user=users[0])

        with self.assertNumQueries(2):
            res = self.client.get(self.about_me_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["id"], users[0].id)

    def test_about_me_staff(self):
        users = [UserFactory(role=RoleChoices.STAFF) for _ in range(5)]

        self.client.force_authenticate(user=users[0])

        with self.assertNumQueries(2):
            res = self.client.get(self.about_me_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["id"], users[0].id)

    def test_create_customer(self):
        user1 = UserFactory(role=RoleChoices.STAFF)

        self.client.force_authenticate(user=user1)

        payload = {
            "username": "user3",
            "role": RoleChoices.CUSTOMER,
            "email": "user3@example.com",
            "phone": "+375291234567",
            "photo": generate_image_file(),
        }

        with self.assertNumQueries(2):
            res = self.client.post(self.list_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_create_staff(self):
        user2 = UserFactory(role=RoleChoices.STAFF)

        self.client.force_authenticate(user=user2)

        payload = {
            "username": "user4",
            "role": RoleChoices.STAFF,
            "email": "user4@example.com",
            "phone": "+375291234567",
            "photo": generate_image_file(),
        }

        with self.assertNumQueries(2):
            res = self.client.post(self.list_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_create_customer_error(self):
        user1 = UserFactory(role=RoleChoices.CUSTOMER)

        self.client.force_authenticate(user=user1)

        payload = {
            "username": "user3",
            "role": RoleChoices.CUSTOMER,
            "email": "user3@example.com",
            "phone": "+375291234567",
            "photo": generate_image_file(),
        }

        with self.assertNumQueries(0):
            res = self.client.post(self.list_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 1)
