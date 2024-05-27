from django.contrib import admin

from sneakers_shop.models import (Carts, OrderDetail, Orders, Payments,
                                  Sneakers, SneakersCategories)

admin.site.register([Orders, OrderDetail, Sneakers, SneakersCategories, Payments, Carts])
