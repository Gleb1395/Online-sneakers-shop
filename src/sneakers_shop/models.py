import os
import random
from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from faker import Faker

from sneakers_shop.utils.data_generators import (
    get_random_assignment, get_random_brand, get_random_categories_sneakers,
    get_random_color, get_random_size)


class Orders(models.Model):
    """
    This model represents an order placed by a user. Each order is associated with a specific user.
    """

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
    """
    Represents the details of a specific order, including the quantity of items and the price for each order.
    """

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
    """
    Represents sneakers with attributes such as color, assignment,
    brand, price, and stock-keeping unit (SKU). Each pair can be linked to an order detail,
    and the sneakers are uniquely identified by a slug for URL purposes.
    """

    order_detail = models.ForeignKey(
        to="sneakers_shop.OrderDetail",
        related_name="sneakers",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    color_sneakers = models.CharField(max_length=120, blank=True, null=True, verbose_name="Sneakers Color")
    assignment_sneakers = models.CharField(max_length=120, blank=True, null=True, verbose_name="Assignment Sneakers")
    brand_sneakers = models.CharField(max_length=120, blank=True, null=True, verbose_name="Sneakers Brand")
    stock_keeping_unit = models.IntegerField(unique=True, blank=True, null=True, verbose_name="stock_keeping_unit")
    price_sneakers = models.FloatField(
        blank=True, null=True, validators=[MinValueValidator(0.0)], verbose_name="Sneakers Price"
    )
    slug = models.SlugField(unique=True, null=True, blank=False)
    image_sneakers = models.ImageField(blank=True, null=True, upload_to="media/sneakers/")
    quantity_sneakers = models.PositiveSmallIntegerField(default=0, verbose_name="Sneakers Quantity")
    description_sneakers = models.TextField(
        default="A description will be coming soon", verbose_name="Sneakers Description"
    )

    def __str__(self):
        return f"{self.brand_sneakers} {self.color_sneakers} {self.assignment_sneakers}"

    @classmethod
    def create_sneakers(cls, count):
        """
        Creating test data
        """

        images_path = "src/media/media/sneakers"
        image_files = os.listdir(images_path)

        for _ in range(count):
            random_image = random.choice(image_files)
            stock_keeping_unit = random.randint(1, 999_999)
            category_sneakers = get_random_categories_sneakers()
            brand_sneakers = get_random_brand()
            sneakers = Sneakers.objects.create(
                order_detail=None,
                color_sneakers=get_random_color(),
                assignment_sneakers=get_random_assignment(),
                brand_sneakers=brand_sneakers,
                price_sneakers=round(random.uniform(8, 200), 2),
                image_sneakers=os.path.join("media/sneakers/", random_image),
                stock_keeping_unit=stock_keeping_unit,
                slug=slugify(f"{brand_sneakers}-{stock_keeping_unit}"),
                quantity_sneakers=50,
            )
            sneakers.save()

            category, _ = SneakersCategories.objects.get_or_create(category_sneakers=category_sneakers)
            SneakersToCategories.objects.create(sneakers=sneakers, categories=category)
            sneakers.save()

            for _ in range(random.randint(2, 5)):
                size_value = get_random_size()
                size, _ = SneakersSize.objects.get_or_create(size=size_value)
                SneakersToSizes.objects.create(sneakers=sneakers, size=size)
                sneakers.save()


class SneakersCategories(models.Model):
    """
    Represents the categories associated with sneakers, allowing each sneaker to belong to multiple categories.
    Each category is linked to a specific pair of sneakers and has a slug for URL purposes.
    """

    category_sneakers = models.CharField(
        max_length=120,
        blank=True,
        null=True,
    )
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return f"{self.category_sneakers}"


class SneakersSize(models.Model):
    """
    Represents the different sizes available for a specific pair of sneakers.
    Each size is linked to a particular sneaker model.
    """

    size = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="sneakers_size")

    def __str__(self):
        return f"{self.size}"


class SneakersToSizes(models.Model):
    """
    Represents the many-to-many relationship between Sneakers and Sizes.
    """

    sneakers = models.ForeignKey(to="sneakers_shop.Sneakers", on_delete=models.CASCADE, related_name="size_relations")
    size = models.ForeignKey(to="sneakers_shop.SneakersSize", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sneakers} - {self.size}"


class SneakersToCategories(models.Model):
    """
    Represents the many-to-many relationship between Sneakers and Categories.
    """

    sneakers = models.ForeignKey(
        to="sneakers_shop.Sneakers", on_delete=models.CASCADE, related_name="category_relations"
    )
    categories = models.ForeignKey(to="sneakers_shop.SneakersCategories", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.categories} - {self.sneakers}"


class Payments(models.Model):
    """
    Represents the payment details for an order. Each payment is linked to a specific order
    and contains information such as the payment amount, date, and method.
    """

    order = models.OneToOneField(to="sneakers_shop.Orders", related_name="payments", on_delete=models.CASCADE)
    amount = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.payment_method}"


class Carts(models.Model):
    """
    Represents a shopping cart containing sneakers added by a user.
    Each cart item tracks the number of sneakers, total price,
    and the date when the item was added to the cart.
    """

    sneakers = models.ForeignKey(to="sneakers_shop.Sneakers", related_name="carts", on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), related_name="user", on_delete=models.CASCADE)
    count_cart = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])
    cart_date = models.DateField(blank=True, null=True)
    selected_size = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.sneakers} {self.total_price} {self.selected_size}"


class Wishlists(models.Model):
    """
    Represents a wishlist where users can save sneakers they are interested in purchasing later.
    Each wishlist entry links a user to a specific product (sneakers).
    """

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name="User")
    product = models.ForeignKey(to="sneakers_shop.Sneakers", on_delete=models.CASCADE, verbose_name="Product")

    def __str__(self):
        return f"{self.user} - {self.product}"
