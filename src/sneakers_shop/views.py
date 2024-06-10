from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from sneakers_shop.models import Sneakers


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


class ShopListView(ListView):
    model = Sneakers  # ????????????
    template_name = "shop.html"
    context_object_name = "sneakers"
    paginate_by = 9


class CartListView(TemplateView):
    template_name = "cart.html"

class PriceView(TemplateView):
    template_name = "price.html"