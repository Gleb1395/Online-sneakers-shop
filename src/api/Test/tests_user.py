from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from sneakers_shop.utils.samples_client import exemple_client


class TestApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_1 = exemple_client(first_name="Test first name", last_name="Test last name", email="email@test1.com")
        self.user_2 = exemple_client(
            first_name="Test 2 first name", last_name="Test 2 last name", email="email@test2.com"
        )

    def test_user(self):
        result = self.client.get(reverse("api:list_clients-list"), kwargs={"pk": self.user_1.pk})
        self.assertEqual(
            result.data[0],
            {
                "first_name": "Test first name",
                "last_name": "Test last name",
                "email": "email@test1.com",
                "is_staff": True,
                "is_active": True,
            },
        )

    def test_user_create_client(self):
        result = self.client.get(reverse("api:list_clients-list"))
        self.assertEqual(len(result.data), 2)
        new_user = {
            "first_name": "Test 3 first name",
            "last_name": "Test 3 last name",
            "email": "Test@email3.com",
            "is_staff": True,
            "is_active": True,
        }
        self.client.post(reverse("api:create_client-list"), new_user, format="json")
        result = self.client.get(reverse("api:list_clients-list"))
        self.assertEqual(len(result.data), 3)

    def test_user_update_client(self):
        result = self.client.get(reverse("api:list_clients-list"), kwargs={"pk": self.user_1.pk})
        print(result.data[0])
        self.assertEqual(
            result.data[0],
            {
                "first_name": "Test first name",
                "last_name": "Test last name",
                "email": "email@test1.com",
                "is_staff": True,
                "is_active": True,
            },
        )
        updated_user = {"first_name": "Test user updete name", "email": "update-date@test1.com"}
        self.client.patch(
            reverse("api:update_client-detail", kwargs={"pk": self.user_1.pk}), updated_user, format="json"
        )
        result = self.client.get(reverse("api:list_clients-list"), kwargs={"pk": self.user_1.pk})
        self.assertEqual(
            result.data[0],
            {
                "first_name": "Test user updete name",
                "last_name": "Test last name",
                "email": "update-date@test1.com",
                "is_staff": True,
                "is_active": True,
            },
        )

    def test_delete_client(self):

        result = self.client.get(reverse("api:list_clients-list"))
        self.assertEqual(len(result.data), 2)

        self.client.delete(reverse("api:delete_client-detail", kwargs={"pk": self.user_1.pk}))
        result = self.client.get(reverse("api:list_clients-list"))
        self.assertEqual(len(result.data), 1)
        self.assertEqual(
            result.data[0],
            {
                "first_name": "Test 2 first name",
                "last_name": "Test 2 last name",
                "email": "email@test2.com",
                "is_staff": True,
                "is_active": True,
            },
        )
