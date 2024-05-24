from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from api.views import ClientViewSet, ClientListViewSet, ClientRetrieveAPIView, ClientRetrieveUpdateAPIView, \
    ClientRetrieveDestroyAPIView
from sneakers_shop.views import AboutView, IndexView, ShopDetailView

app_name = "api"
router = routers.DefaultRouter()
router.register('clients', ClientViewSet, basename='clients')
router.register('list-clients', ClientListViewSet, basename='list-clients')
router.register('retrieve-client', ClientRetrieveAPIView, basename='retrieve-client')
router.register('retrieve-client-update', ClientRetrieveUpdateAPIView, basename='retrieve-client-update')
router.register('retrieve-client-destroy', ClientRetrieveDestroyAPIView, basename='retrieve-client-destroy')



urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
