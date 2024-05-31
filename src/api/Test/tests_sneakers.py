from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sneakers_shop.models import Sneakers
from sneakers_shop.utils.samples_sneakers import (semple_sneakers,
                                                  sneakers_data_all)


class TestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sneakers = semple_sneakers(brand_sneakers="Test sneakers")

    def test_sneakers(self):
        result = self.client.get(reverse("api:detail_sneakers-detail", kwargs={"pk": self.sneakers.pk}))
        self.assertEqual(
            result.data,
            {
                "order_detail": None,
                "size_sneakers": 45,
                "color_sneakers": "blue",
                "brand_sneakers": "Test sneakers",
                "price_sneakers": 12.4,
            },
        )

    def test_sneakers_create_item(self):
        result = self.client.get(reverse("api:list_sneakers-list"))
        self.assertEqual(len(result.data), 1)
        data_new_sneakers = sneakers_data_all(brand_sneakers="Test create item")
        result = self.client.post(reverse("api:create_sneakers-list"), data_new_sneakers, format="json")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.get(reverse("api:list_sneakers-list"))
        self.assertEqual(len(result.data), 2)

    def test_sneakers_create_valid_data(self):
        result = self.client.get(reverse("api:list_sneakers-list"))
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        wrong_data = {"price_sneakers": "asdasd"}
        result = self.client.post(reverse("api:create_sneakers-list"), wrong_data, format="json")
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    #
    def test_sneakers_delete_for_id(self):
        data_sneakers = semple_sneakers(brand_sneakers="Test sneakers brand")
        result = self.client.get(reverse("api:list_sneakers-list"))
        self.assertEqual(len(result.data), 2)
        self.client.delete(reverse("api:delete_sneakers-detail", kwargs={"pk": 1}))
        result = self.client.get(reverse("api:list_sneakers-list"))
        self.assertEqual(len(result.data), 1)

    #
    def test_sneakers_update_item(self):
        result = self.client.get(reverse("api:detail_sneakers-detail", kwargs={"pk": self.sneakers.pk}))
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        update_data = {"brand_sneakers": "Test", "price_sneakers": 124.5}
        result = self.client.patch(
            reverse("api:update_sneakers-detail", kwargs={"pk": self.sneakers.pk}), update_data, format="json"
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data["brand_sneakers"], "Test")
        self.assertEqual(result.data["price_sneakers"], 124.5)
