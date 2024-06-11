from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

import blog
from config.settings import dev
from sneakers_shop import views
from sneakers_shop.views import (AboutView, CartListView, ContactUsView,
                                 IndexView, ServicesView, ShopDetailView,
                                 ShopListView)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("detail/", ShopDetailView.as_view(), name="detail"),
    path("service/", ServicesView.as_view(), name="service"),
    path("contact-us/", ContactUsView.as_view(), name="contact-us"),
    path("shop/", ShopListView.as_view(), name="shop"),
    path("cart/", CartListView.as_view(), name="cart"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("docs-swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("filter-prices/", views.get_value_filter, name="filter_prices"),
    # path("blog", include(blog.urls)),
] + static(dev.MEDIA_URL, document_root=dev.MEDIA_ROOT)
