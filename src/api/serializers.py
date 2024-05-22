from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ListSerializer


# class CustomerSerializer(ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['first_name', 'last_name', 'email', "is_staff", "is_active"]


class OrderDetailsSerializer(ListSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'order', 'quantity', 'price')