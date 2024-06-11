from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

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
    model = Sneakers
    template_name = "shop.html"
    context_object_name = "sneakers"
    paginate_by = 9


def get_value_filter(request):
    if request.method == "POST":
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        show_sneakers = Sneakers.objects.filter(price_sneakers__range=(min_price, max_price))
        context = {"sneakers": show_sneakers, "min_price": min_price, "max_price": max_price}
    return render(request, "shop.html", context)


class CartListView(TemplateView):
    template_name = "cart.html"  # new comment
