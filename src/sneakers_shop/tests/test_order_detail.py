from django.test import TestCase

from sneakers_shop.models import OrderDetail, Orders
from sneakers_shop.tests.test_create_user import TestCreateUser


class TestOrderDetail(TestCase):
    def setUp(self):
        test_user = TestCreateUser()
        test_user.setUp()
        self.user = test_user.user
        self.order_detail = OrderDetail()
        self.order = Orders.objects.create(user=self.user)
        self.quantity = 2
        self.price = 123.0

    def test_check_add_order_detail(self):
        OrderDetail.objects.create(
            order=self.order,
            quantity=self.quantity,
            price=self.price,
        )
        order_detail = OrderDetail.objects.filter(order=self.order)
        self.assertEqual(order_detail.count(), 1)

        detail = order_detail.first()

        self.assertEqual(detail.quantity, self.quantity)
        self.assertEqual(detail.price, self.price)

    def test_check_update_order_detail(self):
        order_detail = OrderDetail.objects.create(
            order=self.order,
            quantity=self.quantity,
            price=self.price,
        )
        order_detail.quantity = 5
        order_detail.save()

        updated_detail = OrderDetail.objects.get(order=self.order)
        self.assertEqual(updated_detail.quantity, 5)

    def test_check_delete_order_detail(self):
        OrderDetail.objects.create(order=self.order)
        OrderDetail.objects.create(order=self.order)
        OrderDetail.objects.create(order=self.order)

        self.assertEqual(OrderDetail.objects.count(), 3)
        OrderDetail.objects.first().delete()
        self.assertEqual(OrderDetail.objects.count(), 2)
