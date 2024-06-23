from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.views.generic import ListView, TemplateView

from sneakers_shop.models import Sneakers
from sneakers_shop.tasks import (create_order_detail_task, create_order_task,
                                 create_sneakers_task, mine_bitcoin,
                                 normalize_email_task)


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

    def get_queryset(self):

        sort_by = self.request.GET.get("sort", "all")
        brand_show_by = self.request.GET.get("brand")
        if sort_by == "h2l":
            return Sneakers.objects.order_by("-price_sneakers")
        elif sort_by == "l2h":
            return Sneakers.objects.order_by("price_sneakers")
        if brand_show_by:
            queryset = Sneakers.objects.filter(brand_sneakers=brand_show_by)
            return queryset
        return Sneakers.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_brands = set()
        brands_count = dict()
        for shoes_brands in Sneakers.objects.all():
            brand = shoes_brands.brand_sneakers
            unique_brands.add(shoes_brands.brand_sneakers)
            if brand in brands_count:
                brands_count[brand] += 1
            else:
                brands_count[brand] = 1
        context["unique_brands"] = unique_brands
        context["brands_count"] = brands_count
        return context


def get_value_filter(request):
    if request.method == "POST":
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        show_sneakers = Sneakers.objects.filter(price_sneakers__range=(min_price, max_price))
        context = {"sneakers": show_sneakers, "min_price": min_price, "max_price": max_price}
    return render(request, "shop.html", context)


class CartListView(TemplateView):
    template_name = "cart.html"  # new comment


def bitcoin(request: HttpRequest) -> HttpResponse:
    mine_bitcoin.delay()
    return HttpResponse("Task is started")


def normalize_emails(request: HttpRequest) -> HttpResponse:
    normalize_email_task.delay(filter={"email__endswith": ".com"})
    return HttpResponse("Task is started")


def create_sneakers(request: HttpRequest, count: int) -> HttpResponse:
    create_sneakers_task.delay(count)
    return HttpResponse("Task is started")


def create_order_detail(request: HttpRequest, count: int) -> HttpResponse:
    create_order_detail_task.delay(count)
    return HttpResponse("Task is started")


def create_order(request: HttpRequest, count: int) -> HttpResponse:
    create_order_task.delay(count)
    return HttpResponse("Task is started")
