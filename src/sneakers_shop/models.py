import random
from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from faker import Faker


class Orders(models.Model):
    user = models.ForeignKey(to=get_user_model(), related_name="orders", on_delete=models.CASCADE)
    order_date = models.DateField(blank=True, null=True)
    order_status = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.order_date} {self.order_status}"

    @classmethod
    def create_order(cls, count):
        faker = Faker()
        for i in range(count):
            order = Orders.objects.create(
                user=get_user_model().objects.get(id=1),
                order_date=faker.date_between(start_date=date(2020, 5, 13), end_date=date(2023, 5, 13)),
                order_status=True,
            )
            order.save()


class OrderDetail(models.Model):
    order = models.ForeignKey(to="sneakers_shop.Orders", related_name="order_detail", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"{self.order} {self.quantity} {self.price}"

    @classmethod
    def create_order_detail(cls, count):
        for i in range(count):
            order_detail = OrderDetail.objects.create(
                order=Orders.objects.get(id=1),
                quantity=random.randrange(1, 5),
                price=random.uniform(10.0, 25.5),
            )
            order_detail.save()


class Sneakers(models.Model):
    order_detail = models.ForeignKey(
        to="sneakers_shop.OrderDetail",
        related_name="sneakers",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    size_sneakers = models.PositiveSmallIntegerField(blank=True, null=True)
    color_sneakers = models.CharField(max_length=120, blank=True, null=True)
    model_sneakers = models.CharField(max_length=120, blank=True, null=True)
    brand_sneakers = models.CharField(max_length=120, blank=True, null=True)
    price_sneakers = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])
    image_sneakers = models.ImageField(blank=True, null=True, upload_to="media/sneakers/")

    def __str__(self):
        return f"{self.size_sneakers} {self.brand_sneakers} {self.color_sneakers}"

    @classmethod
    def create_sneakers(cls, count):
        for _ in range(count):
            sneakers = Sneakers.objects.create(
                order_detail=None,
                size_sneakers=random.randrange(37, 45),
                color_sneakers="Red",
                model_sneakers=f"Sport {random.randrange(1, 5)}",
                brand_sneakers="Nike",
                price_sneakers=random.uniform(10.0, 25.0),
            )
            sneakers.save()


class SneakersCategories(models.Model):
    sneakers = models.ForeignKey(
        to="sneakers_shop.Sneakers", related_name="sneakers_categories", on_delete=models.CASCADE
    )
    category_sneakers = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f"{self.category_sneakers}"


class Payments(models.Model):
    order = models.OneToOneField(to="sneakers_shop.Orders", related_name="payments", on_delete=models.CASCADE)
    amount = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.payment_method}"


class Carts(models.Model):
    sneakers = models.ForeignKey(to="sneakers_shop.Sneakers", related_name="carts", on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), related_name="carts", on_delete=models.CASCADE)
    count_cart = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])
    cart_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.total_price} {self.cart_date}"
