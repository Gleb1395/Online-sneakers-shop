from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.permissions import IsSuperUser
from api.serializers import (CustomerSerializer, OrderDetailsSerializer,
                             OrdersSerializer, SneakersSerializer)
from sneakers_shop.models import OrderDetail, Orders, Sneakers


class ClientCreateAPIView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class ClientRetrieveDestroyAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class ClientRetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class ClientListAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class OrderCreateAPIView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrderRetrieveDestroyAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrderRetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrderListAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrderDetailCreateAPIView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer


class OrderDetailRetrieveDestroyAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer


class OrderDetailRetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer


class OrderDetailListAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer


class SneakersCreateAPIView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Sneakers.objects.all()
    serializer_class = SneakersSerializer


class SneakersRetrieveDestroyAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Sneakers.objects.all()
    serializer_class = SneakersSerializer


class SneakersRetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Sneakers.objects.all()
    serializer_class = SneakersSerializer


class SneakersListAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Sneakers.objects.all()
    serializer_class = SneakersSerializer


class SneakersDetailAPIView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Sneakers.objects.all()
    serializer_class = SneakersSerializer
