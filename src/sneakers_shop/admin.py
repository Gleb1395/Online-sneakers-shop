from django.contrib import admin
from django.contrib.auth import get_user_model

from sneakers_shop.models import (Carts, OrderDetail, Orders, Payments,
                                  Sneakers, SneakersCategories)

admin.site.register([Orders, OrderDetail, Sneakers, SneakersCategories, Payments, Carts, get_user_model()])
