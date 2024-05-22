from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

# from api.views import ClientViewSet
from sneakers_shop.views import AboutView, IndexView, ShopDetailView

app_name = "api"
router = routers.DefaultRouter()
# router.register('clients', ClientViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
