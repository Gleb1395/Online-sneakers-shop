from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from api.views import (ClientCreateAPIView, ClientListAPIView,
                       ClientRetrieveDestroyAPIView,
                       ClientRetrieveUpdateAPIView, OrderCreateAPIView,
                       OrderDetailCreateAPIView, OrderDetailListAPIView,
                       OrderDetailRetrieveDestroyAPIView,
                       OrderDetailRetrieveUpdateAPIView, OrderListAPIView,
                       OrderRetrieveDestroyAPIView, OrderRetrieveUpdateAPIView,
                       SneakersCreateAPIView, SneakersListAPIView,
                       SneakersRetrieveDestroyAPIView,
                       SneakersRetrieveUpdateAPIView)
from sneakers_shop.views import AboutView, IndexView, ShopDetailView

app_name = "api"
router = routers.DefaultRouter()
router.register("create-client", ClientCreateAPIView, basename="create_client")
router.register("delete-client", ClientRetrieveDestroyAPIView, basename="delete_client")
router.register("update-client", ClientRetrieveUpdateAPIView, basename="update_client")
router.register("list-clients", ClientListAPIView, basename="list_clients")

router.register("create-order", OrderCreateAPIView, basename="create_order")
router.register("delete-order", OrderRetrieveDestroyAPIView, basename="delete_order")
router.register("update-order", OrderRetrieveUpdateAPIView, basename="update_order")
router.register("list-orders", OrderListAPIView, basename="list_orders")

router.register("create-order-detail", OrderDetailCreateAPIView, basename="create_order_detail")
router.register("delete-order-detail", OrderDetailRetrieveDestroyAPIView, basename="delete_order_detail")
router.register("update-order-detail", OrderDetailRetrieveUpdateAPIView, basename="update_order_detail")
router.register("list-orders-detail", OrderDetailListAPIView, basename="list_orders_detail")

router.register("create-sneakers", SneakersCreateAPIView, basename="create_sneakers")
router.register("delete-sneakers", SneakersRetrieveDestroyAPIView, basename="delete_sneakers")
router.register("update-sneakers", SneakersRetrieveUpdateAPIView, basename="update_sneakers")
router.register("list-sneakers", SneakersListAPIView, basename="list_sneakers")


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
