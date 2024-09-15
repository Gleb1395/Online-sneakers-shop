import math
from datetime import date

import requests
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Max, Min, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import register
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, View)
from webargs import fields
from webargs.djangoparser import use_args

from sneakers_shop.forms import (CartAddForm, UserLoginForm,
                                 UserRegistrationForm)
from sneakers_shop.models import (Carts, Sneakers, SneakersCategories,
                                  SneakersSize, Wishlists)


class IndexView(TemplateView):
    """
    A view for displaying the home page of the site
    """

    template_name = "index.html"


class AboutView(TemplateView):
    """
    A simple view that renders the 'About'.
    """

    template_name = "about.html"


class ServicesView(TemplateView):
    """
    A view that renders the 'Services'.
    """

    template_name = "service.html"


class ContactUsView(TemplateView):
    """
    A view that renders the 'Contact Us'.
    """

    template_name = "contact_us.html"


class ShopListView(ListView):
    """
    A view that displays a paginated list of sneakers.
    """

    model = Sneakers
    template_name = "shop.html"
    context_object_name = "sneakers"
    paginate_by = 18

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    @use_args(
        {
            "sort": fields.Str(required=False),
            "brand_sneakers": fields.Str(required=False),
            "assignment_sneakers": fields.Str(required=False),
            "filter_cleaning": fields.Str(required=False),
            "min_price": fields.Integer(required=False),
            "max_price": fields.Integer(required=False),
            "color_sneakers": fields.Str(required=False),
            "size": fields.Str(required=False),
            "category": fields.Str(required=False),
        },
        location="query",
    )
    def get_queryset(self, params):
        sneakers = Sneakers.objects.all()

        filters = {}
        search_fields = [
            "brand_sneakers",
            "assignment_sneakers",
            "sort",
            "min_price",
            "max_price",
            "color_sneakers",
            "size",
            "category",
        ]
        or_filter = Q()
        sorted_by = params.get("sort")
        min_price = self.request.POST.get("min_price")
        max_price = self.request.POST.get("max_price")
        search = self.request.POST.get("search")

        if search:
            sneakers = Sneakers.objects.filter(
                Q(color_sneakers__icontains=search)  # NOQA W503
                | Q(assignment_sneakers__icontains=search)  # NOQA W503
                | Q(brand_sneakers__icontains=search)  # NOQA W503
            )
            return sneakers

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

            for key, value in self.request.session.items():

                if key == "wishlist" or key == "cart":
                    continue
                if key.startswith("_"):
                    continue
                elif key == "min_price":
                    or_filter &= Q(price_sneakers__gte=value)
                    continue
                elif key == "max_price":
                    or_filter &= Q(price_sneakers__lte=value)
                    continue
                elif key == "sort":
                    sorted_by = value
                    continue
                elif key == "size":
                    or_filter &= Q(size_relations__size__size=value)
                    continue
                elif key == "category":
                    or_filter &= Q(category_relations__categories__category_sneakers=value)
                    continue
                else:
                    or_filter &= Q(**{key: value})
        if sorted_by:
            queryset = sneakers.filter(or_filter).order_by(sorted_by)
        else:
            queryset = sneakers.filter(or_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_brands = set()
        unique_assignment = set()
        unique_color = set()
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

        for shoes in Sneakers.objects.all():
            brand = shoes.brand_sneakers
            unique_brands.add(shoes.brand_sneakers)
            unique_assignment.add(shoes.assignment_sneakers)
            unique_color.add(shoes.color_sneakers)
            if brand in brands_count:
                brands_count[brand] += 1
            else:
                brands_count[brand] = 1

        context.update(
            {
                "unique_brands": sorted(unique_brands),
                "brands_count": brands_count,
                "count_brands": count_brands,
                "unique_assignment": list(unique_assignment),
                "unique_color": list(unique_color),
                "unique_sizes": SneakersSize.objects.all().order_by("size"),
                "db_min_price": math.ceil(db_min_price),
                "db_max_price": math.ceil(db_max_price),
                "user_min_price": math.floor(user_min_price),
                "user_max_price": math.floor(user_max_price),
            }
        )
        return context


class SneakersDetailView(DetailView):
    model = Sneakers
    context_object_name = "sneakers"
    template_name = "shop-detail.html"

    def get_queryset(self):
        queryset = Sneakers.objects.filter(slug=self.kwargs["slug"])
        if queryset.exists():
            return Sneakers.objects.filter(slug=self.kwargs["slug"])
        else:
            raise Http404


class CartListView(ListView):
    model = Carts
    template_name = "cart.html"
    context_object_name = "carts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        coupon = self.request.GET.get("coupon")
        dict_discount = {"Bonus": 5, "Express": 10, "Save": 8, "Flash": 15, "Favorite": 25}

        if self.request.user.is_authenticated:
            carts = Carts.objects.filter(user=self.request.user)
            context["carts"] = carts
            total_price = sum(cart.total_price for cart in carts)
            if coupon in dict_discount.keys():
                context["coupon"] = dict_discount[coupon]
                discount = total_price * (int(dict_discount[coupon]) / 100)
                total_price_with_discount = total_price - discount
                context["total_price_with_discount"] = total_price_with_discount
            context["total_price"] = total_price

        else:
            cart = self.request.session.get("cart", {})
            context["carts"] = cart.values()
            total_price = sum(item["total_price"] for item in cart.values())
            if coupon in dict_discount.keys():
                context["coupon"] = dict_discount[coupon]
                discount = total_price * (int(dict_discount[coupon]) / 100)
                total_price_with_discount = total_price - discount
                context["total_price_with_discount"] = total_price_with_discount

        context["form"] = CartAddForm()
        context["total_price"] = total_price
        return context


class CartAddView(View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get("slug")
        product = get_object_or_404(Sneakers, slug=product_slug)
        selected_size = request.GET.get("selected_size")

        if request.user.is_authenticated:
            cart_item, created = Carts.objects.get_or_create(
                user=request.user,
                sneakers=product,
                selected_size=selected_size,
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
            categories = product.category_relations.all()
            categories_name = " ,".join(cat.categories.category_sneakers for cat in categories)

            if str(product_slug) in cart:
                cart[str(product_slug)]["count"] += 1
                cart[str(product_slug)]["total_price"] += product.price_sneakers
                cart[str(product_slug)]["size"] = selected_size
            else:
                cart[str(product_slug)] = {
                    "product_slug": product_slug,
                    "count": 1,
                    "total_price": product.price_sneakers,
                    "category": categories_name,
                    "brand_sneakers": product.brand_sneakers,
                    "image_sneakers": product.image_sneakers.url if product.image_sneakers else None,
                    "price": product.price_sneakers,
                    "assignment": product.assignment_sneakers,
                    "color": product.color_sneakers,
                    "size": selected_size,
                }
            request.session["cart"] = cart
        return redirect("cart")

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        product_slug = kwargs.get("slug")
        if action == "remove":
            if request.user.is_authenticated:
                cart_item = Carts.objects.filter(user=request.user, sneakers__slug=product_slug)
                if cart_item:
                    cart_item.delete()
                else:
                    pass
            else:
                cart = request.session.get("cart", {})
                if str(product_slug) in cart:
                    del cart[str(product_slug)]
                    request.session["cart"] = cart
        return redirect("cart")


class UserRegistrationView(CreateView):
    template_name = "sign_up.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    template_name = "sign_in.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")


class WishlistAddView(View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get("slug")
        product = get_object_or_404(Sneakers, slug=product_slug)

        categories = product.category_relations.all()
        categories_name = " ,".join(cat.categories.category_sneakers for cat in categories)

        if request.user.is_authenticated:
            wish_item, created = Wishlists.objects.get_or_create(
                user=request.user,
                product=product,
            )
            if not created:
                wish_item.save()
        else:
            wishlist = request.session.get("wishlist", {})
            wishlist[str(product_slug)] = {
                "product_slug": product_slug,
                "category": categories_name,
                "brand_sneakers": product.brand_sneakers,
                "image_sneakers": product.image_sneakers.url if product.image_sneakers else None,
                "assignment": product.assignment_sneakers,
                "price": product.price_sneakers,
                "color": product.color_sneakers,
            }
            request.session["wishlist"] = wishlist
        return redirect("wishlist")

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        product_slug = kwargs.get("slug")

        if action == "remove":
            if request.user.is_authenticated:
                wishlist = Wishlists.objects.filter(user=request.user, product__slug=product_slug)
                wishlist.delete()
            else:
                wishlist = request.session.get("wishlist", {})
                if str(product_slug) in wishlist:
                    del wishlist[str(product_slug)]
                    request.session["wishlist"] = wishlist
        return redirect("wishlist")


class WishListView(ListView):
    model = Wishlists
    template_name = "wishlist.html"
    context_object_name = "wishlists"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["wishlists"] = Wishlists.objects.filter(user=self.request.user)
        else:
            wishlist = self.request.session.get("wishlist", {})
            context["wishlist"] = wishlist.values()

        return context


def debug_view(request):
    sorted_sneakers = Sneakers.objects.filter(size_relations__size__size=41).prefetch_related("size_relations__size")
    for sneaker in sorted_sneakers:
        print(f"{sneaker}")
    return render(request, "debug_tamplate.html")
