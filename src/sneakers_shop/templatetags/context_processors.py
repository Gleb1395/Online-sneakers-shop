from sneakers_shop.models import Carts


def cart_badge(request):
    badge = 0
    if request.user.is_authenticated:
        carts = Carts.objects.filter(user=request.user)
        badge = sum(cart.count_cart for cart in carts)
    else:
        cart = request.session.get("cart", {})
        badge = sum(item["count"] for item in cart.values())
    return {"badge": badge}


def cart_product(request):
    cart = request.session.get("cart", {})
    return {"product": cart}


def cart_total_price(request):
    if request.user.is_authenticated:
        carts = Carts.objects.filter(user=request.user)
        total_price = sum(item["total_price"] for item in carts.values())
    else:
        cart = request.session.get("cart", {})
        total_price = sum(item["total_price"] for item in cart.values())
    return {"price": total_price}
