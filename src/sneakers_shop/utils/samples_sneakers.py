from sneakers_shop.models import Sneakers


def semple_sneakers(brand_sneakers: str, **params):
    default = {
        "order_detail": None,
        "size_sneakers": 45,
        "color_sneakers": "blue",
        "brand_sneakers": "Adidas",
        "price_sneakers": 12.4,
    }
    default.update(params)
    default["brand_sneakers"] = brand_sneakers
    return Sneakers.objects.create(**default)


#
def sneakers_data_all(brand_sneakers: str, **params):
    default = {
        "order_detail": None,
        "size_sneakers": 31,
        "color_sneakers": "Yellow",
        "brand_sneakers": "PUMA",
        "price_sneakers": 701.2,
    }
    default.update(params)
    default["brand_sneakers"] = brand_sneakers
    return default
