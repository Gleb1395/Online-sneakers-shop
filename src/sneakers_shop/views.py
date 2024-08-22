import math
from datetime import date

import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Max, Min, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import register
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, View)
from webargs import fields
from webargs.djangoparser import use_args

from sneakers_shop.forms import CartAddForm, UserRegistrationForm
from sneakers_shop.models import Carts, Sneakers


class IndexView(TemplateView):
    """
    Представление для отображения главной страницы сайта
    """

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
    paginate_by = 12

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    @use_args(
        {
            "sort": fields.Str(required=False),
            "brand_sneakers": fields.Str(required=False),
            "model_sneakers": fields.Str(required=False),
            "filter_cleaning": fields.Str(required=False),
            "min_price": fields.Integer(required=False),
            "max_price": fields.Integer(required=False),
            "color_sneakers": fields.Str(required=False),
            "size_sneakers": fields.Str(required=False),
        },
        location="query",
    )
    def get_queryset(self, params):
        sneakers = Sneakers.objects.all()
        filters = {}
        search_fields = [
            "brand_sneakers",
            "model_sneakers",
            "sort",
            "min_price",
            "max_price",
            "color_sneakers",
            "size_sneakers",
        ]
        or_filter = Q()
        sorted_by = params.get("sort")
        min_price = self.request.POST.get("min_price")
        max_price = self.request.POST.get("max_price")

        if min_price and max_price:
            params["min_price"] = min_price
            params["max_price"] = max_price

        if params.get("filter_cleaning") == "clean":
            for field in search_fields:
                self.request.session.pop(field, None)
            sneakers = Sneakers.objects.all()
            return sneakers

        for param_name, param_value in params.items():
            for fileds in search_fields:
                if fileds == param_name:
                    filters[fileds] = param_value
            self.request.session[f"{param_name}"] = filters[param_name]

            for k, v in self.request.session.items():
                if k == "min_price":
                    or_filter &= Q(price_sneakers__gte=v)
                    continue
                if k == "max_price":
                    or_filter &= Q(price_sneakers__lte=v)
                    continue
                if k == "cart":
                    continue
                if k == "sort":
                    sorted_by = v
                else:
                    or_filter &= Q(**{k: v})
        if sorted_by:
            queryset = sneakers.filter(or_filter).order_by(sorted_by)
        else:
            queryset = sneakers.filter(or_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_brands = set()
        unique_models = set()
        unique_color = set()
        unique_sizes = set()
        brands_count = dict()
        sneakers = Sneakers.objects.all()
        count_brands = sneakers.values("brand_sneakers").distinct().count()
        db_min_price = sneakers.values("price_sneakers").aggregate(Min("price_sneakers"))["price_sneakers__min"]
        db_max_price = sneakers.values("price_sneakers").aggregate(Max("price_sneakers"))["price_sneakers__max"]
        if "min_price" in self.request.session and "max_price" in self.request.session:
            user_min_price = int(self.request.session["min_price"])
            user_max_price = int(self.request.session["max_price"])
        else:
            user_min_price = db_min_price
            user_max_price = db_max_price

        for shoe in Sneakers.objects.all():
            brand = shoe.brand_sneakers
            unique_brands.add(shoe.brand_sneakers)
            unique_models.add(shoe.model_sneakers)
            unique_color.add(shoe.color_sneakers)
            unique_sizes.add(shoe.size_sneakers)
            if brand in brands_count:
                brands_count[brand] += 1
            else:
                brands_count[brand] = 1

        context.update(
            {
                "unique_brands": sorted(unique_brands),
                "brands_count": brands_count,
                "count_brands": count_brands,
                "unique_models": list(unique_models),
                "unique_color": list(unique_color),
                "unique_sizes": list(unique_sizes),
                "db_min_price": math.ceil(db_min_price),
                "db_max_price": math.ceil(db_max_price),
                "user_min_price": math.floor(user_min_price),
                "user_max_price": math.floor(user_max_price),
            }
        )
        return context


class CartListView(ListView):
    model = Carts
    template_name = "cart.html"
    context_object_name = "carts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            carts = Carts.objects.filter(user=self.request.user)
            context["carts"] = Carts.objects.filter(user=self.request.user)
            total_price = sum(cart.total_price for cart in carts)
        else:
            cart = self.request.session.get("cart", {})
            context["carts"] = cart.values()
            total_price = sum(item["total_price"] for item in cart.values())

        context["form"] = CartAddForm()
        context["total_price"] = total_price
        return context


class CartAddView(View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product = get_object_or_404(Sneakers, pk=product_id)
        if request.user.is_authenticated:
            cart_item, created = Carts.objects.get_or_create(
                user=request.user,
                sneakers=product,
                defaults={
                    "count_cart": 1,
                    "total_price": product.price_sneakers,
                    "cart_date": date.today(),
                },
            )
            if not created:
                cart_item.count_cart += 1
                cart_item.total_price += product.price_sneakers
                cart_item.save()
        else:
            cart = request.session.get("cart", {})
            if str(product_id) in cart:
                cart[str(product_id)]["count"] += 1
                cart[str(product_id)]["total_price"] += product.price_sneakers
            else:
                cart[str(product_id)] = {
                    "product_id": product_id,
                    "count": 1,
                    "total_price": product.price_sneakers,
                    "model_sneakers": product.model_sneakers,
                    "brand_sneakers": product.brand_sneakers,
                    "image_sneakers": product.image_sneakers.url if product.image_sneakers else None,
                    "price": product.price_sneakers,
                }
            request.session["cart"] = cart
            print(cart)
        return redirect("cart")

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        product_id = kwargs.get("pk")
        if action == "remove":
            if request.user.is_authenticated:
                cart_item = get_object_or_404(Carts, user=request.user, sneakers_id=product_id)
                cart_item.delete()
            else:
                cart = request.session.get("cart", {})
                if str(product_id) in cart:
                    del cart[str(product_id)]
                    request.session["cart"] = cart
        return redirect("cart")


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


class UserRegistrationView(CreateView):
    template_name = "sign_up.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "sign_in.html"
    success_url = reverse_lazy("index")
