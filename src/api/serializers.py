from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from sneakers_shop.models import OrderDetail, Orders, Sneakers


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "is_staff", "is_active"]


class OrdersSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = ["user", "order_date", "order_status"]


class OrderDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ["order", "quantity", "price"]


class SneakersSerializer(ModelSerializer):
    class Meta:
        model = Sneakers
        fields = ["order_detail", "size_sneakers", "color_sneakers", "brand_sneakers", "price_sneakers"]

    @staticmethod
    def validate_size_sneakers(value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Size sneakers must be an integer")
        return value
