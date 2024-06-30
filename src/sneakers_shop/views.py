from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.views.generic import DetailView, ListView, TemplateView
from webargs import fields
from webargs.djangoparser import use_args

from sneakers_shop.models import Sneakers


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ServicesView(TemplateView):
    template_name = "service.html"


class ContactUsView(TemplateView):
    template_name = "contact_us.html"


class ShopListView(ListView):
    model = Sneakers
    template_name = "shop.html"
    context_object_name = "sneakers"
    paginate_by = 9

    @use_args(
        {
            "sort": fields.Str(required=False),
            "brand_sneakers": fields.Str(required=False),
            "model_sneakers": fields.Str(required=False),
        },
        location="query",
    )
    def get_queryset(self, params):
        sneakers = Sneakers.objects.all()
        sort_by = self.request.GET.get("sort", "all")
        search_fields = ["brand_sneakers", "model_sneakers"]  # NOQA F841
        filters = {}
        if "brand_sneakers" in params:
            filters["brand_sneakers"] = params["brand_sneakers"]
        if "model_sneakers" in params:
            filters["model_sneakers"] = params["model_sneakers"]
        if filters:
            sneakers = sneakers.filter(**filters)
        if sort_by == "h2l":
            return Sneakers.objects.order_by("-price_sneakers")
        elif sort_by == "l2h":
            return Sneakers.objects.order_by("price_sneakers")
        return sneakers

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


class SneakersDetailView(DetailView):
    model = Sneakers
    context_object_name = "sneakers"
    template_name = "shop-detail.html"

    def get_queryset(self):
        queryset = Sneakers.objects.filter(id=self.kwargs["pk"])
        if queryset.exists():
            return Sneakers.objects.filter(id=self.kwargs["pk"])
        else:
            raise Http404
