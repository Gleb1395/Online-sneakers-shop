from django.test import TestCase

from sneakers_shop.models import OrderDetail, Orders, Sneakers
from sneakers_shop.tests.test_create_user import TestCreateUser
# Some changes

class TestSneakers(TestCase):
    def setUp(self):
        test_user = TestCreateUser()
        test_user.setUp()
        self.user = test_user.user
        self.orders = Orders.objects.create(user=self.user)
        self.order_detail = OrderDetail.objects.create(order=self.orders)
        self.sneakers = Sneakers()
        self.size_sneakers = 45
        self.color_sneakers = "Red"
        self.model_sneakers = "Sport"
        self.brand_sneakers = "Nike"
        self.price_sneakers = 100.00

    def test_create_sneakers_item(self):
        Sneakers.objects.create(order_detail=self.order_detail)
        self.assertEqual(Sneakers.objects.count(), 1)

        Sneakers.objects.create(order_detail=self.order_detail)
        Sneakers.objects.create(order_detail=self.order_detail)
        self.assertEqual(Sneakers.objects.count(), 3)

    def test_delete_sneakers_(self):
        Sneakers.objects.create(order_detail=self.order_detail)
        Sneakers.objects.create(order_detail=self.order_detail)
        Sneakers.objects.create(order_detail=self.order_detail)
        self.assertEqual(Sneakers.objects.count(), 3)

        Sneakers.objects.all().first().delete()
        self.assertEqual(Sneakers.objects.count(), 2)
