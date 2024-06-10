from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ShopDetailView(TemplateView):
    template_name = "detail.html"


class ServicesView(TemplateView):
    template_name = "service.html"


class ContactUsView(TemplateView):
    template_name = "contact_us.html"


class ShopListView(TemplateView):
    template_name = "shop.html"


class CartListView(TemplateView):
    template_name = "cart.html"
