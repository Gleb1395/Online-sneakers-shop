from django.contrib import admin
from django.contrib.auth import get_user_model

from sneakers_shop.models import (Carts, OrderDetail, Orders, Payments,
                                  Sneakers, SneakersCategories, SneakersSize,
                                  SneakersToCategories, SneakersToSizes)


class SneakersToSizeInline(admin.TabularInline):
    model = SneakersToSizes
    extra = 1


class SneakersToCategoriesInline(admin.TabularInline):
    model = SneakersToCategories
    extra = 1


@admin.register(Sneakers)
class SneakersAdmin(admin.ModelAdmin):
    list_display = ("brand_sneakers", "assignment_sneakers")
    prepopulated_fields = {"slug": ("brand_sneakers", "stock_keeping_unit")}
    inlines = [SneakersToSizeInline, SneakersToCategoriesInline]


admin.site.register([Orders, OrderDetail, SneakersCategories, Payments, Carts, get_user_model(), SneakersSize])
