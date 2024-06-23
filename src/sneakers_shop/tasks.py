import random
import time
from datetime import date

from celery import shared_task
from django.contrib.auth import get_user_model
from faker import Faker

from sneakers_shop.models import OrderDetail, Orders, Sneakers


@shared_task
def mine_bitcoin():
    time.sleep(random.randint(1, 10))


@shared_task
def normalize_email_task(filter):
    users = get_user_model().objects.filter(**filter)
    if users:
        for user in users:
            print(f"working with user:{user.email}")
            user.save()
    else:
        print("no users found")
    return f"Checked{len(users)} users"


@shared_task()
def create_sneakers_task(count):
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
    return f"Created {count} sneakers"


@shared_task()
def create_order_detail_task(count):
    for i in range(count):
        order_detail = OrderDetail.objects.create(
            order=Orders.objects.get(id=1),
            quantity=random.randrange(1, 5),
            price=random.uniform(10.0, 25.5),
        )
        order_detail.save()
    return f"Created {count} order detai"


@shared_task()
def create_order_task(count):
    faker = Faker()
    for i in range(count):
        order = Orders.objects.create(
            user=get_user_model().objects.get(id=1),
            order_date=faker.date_between(start_date=date(2020, 5, 13), end_date=date(2023, 5, 13)),
            order_status=True,
        )
        order.save()
    return f"Created {count} order"
