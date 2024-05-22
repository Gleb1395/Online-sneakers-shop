from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

# from api.serializers import CustomerSerializer
#
#
# class ClientViewSet(ModelViewSet):
#     queryset = get_user_model().objects.all()
#     serializer_class = CustomerSerializer

class OrderDetailsViewSet(ListAPIView):
    queryset = get_user_model().objects.all()
