from django.contrib.auth import get_user_model
from django.test import TestCase

from sneakers_shop.models import Orders
from sneakers_shop.tests.test_create_user import TestCreateUser


class TestOreds(TestCase):
    def setUp(self):
        test_user = TestCreateUser()
        test_user.setUp()
        self.order = Orders()
        self.user = test_user.user
        self.order_date = "2020-05-21"
        self.order_status = True
        Orders.objects.create(user=self.user)
        Orders.objects.create(user=self.user)
        Orders.objects.create(user=self.user)

    def test_check_create_order(self):
        with self.assertRaises(TypeError):
            self.order_date(123)

    def test_check_order_status(self):
        self.order_status = False
        self.assertEqual(self.order_status, False)

        self.order_status = True
        self.assertEqual(self.order_status, True)

    def test_check_order_list(self):
        orders = Orders.objects.filter(user=self.user)
        self.assertEqual(orders.count(), 3)

        for order in orders:
            self.assertEqual(order.user, self.user)


