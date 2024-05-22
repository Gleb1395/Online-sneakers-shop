from django.contrib import admin
from sneakers_shop.models import Orders, OrderDetail, Sneakers, SneakersCategories, Payments, Carts


admin.site.register([Orders, OrderDetail, Sneakers, SneakersCategories, Payments, Carts])