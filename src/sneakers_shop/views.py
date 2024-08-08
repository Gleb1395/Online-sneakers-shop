from datetime import date

from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaulttags import register
from django.views.generic import DetailView, ListView, TemplateView, View
from webargs import fields
from webargs.djangoparser import use_args

from sneakers_shop.forms import CartAddForm
from sneakers_shop.models import Carts, Sneakers


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
        },
        location="query",
    )
    def get_queryset(self, params):
        sneakers = Sneakers.objects.all()
        filters = {}
        search_fields = ["brand_sneakers", "model_sneakers", "sort"]
        or_filter = Q()
        sorted_by = params.get("sort")
        min_price = self.request.POST.get("min_price")
        max_price = self.request.POST.get("max_price")
        print(min_price, max_price)

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
                if k == "cart":
                    pass
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
        brands_count = dict()
        sneakers = Sneakers.objects.all()
        count_brands = sneakers.values("brand_sneakers").distinct().count()
        for shoe in Sneakers.objects.all():
            brand = shoe.brand_sneakers
            unique_brands.add(shoe.brand_sneakers)
            unique_models.add(shoe.model_sneakers)
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
            }
        )
        return context


# def get_value_filter(request):
#     if request.method == "POST":
#         min_price = request.POST.get("min_price")
#         max_price = request.POST.get("max_price")
#         show_sneakers = Sneakers.objects.filter(price_sneakers__range=(min_price, max_price))
#         context = {"sneakers": show_sneakers, "min_price": min_price, "max_price": max_price}
#     return render(request, "shop.html", context)
# def get_value_filter(request): # Нунжо сделать
#
#     view = ShopListView()
#     view.setup(request)
#     view.object_list = view.get_queryset()
#     context = view.get_context_data()
#
#
#     if request.method == "POST":
#         min_price = request.POST.get("min_price")
#         max_price = request.POST.get("max_price")
#         if min_price and max_price:
#             show_sneakers = Sneakers.objects.filter(price_sneakers__range=(min_price, max_price))
#         else:
#             show_sneakers = Sneakers.objects.all()
#         context.update({"min_price": min_price, "max_price": max_price})
#         print(context)
#
#     return render(request, "shop.html", context)


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
