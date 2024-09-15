import random


def get_random_brand():
    list_name_brand_sneakers = [
        "Nike",
        "Adidas",
        "StrideSonic",
        "Puma",
        "Reebok",
        "FlyFusion",
        "New Balance",
        "UrbanGlide",
        "Asics",
        "SwiftStep",
    ]
    return random.choice(list_name_brand_sneakers)


def get_random_assignment():
    list_name_assignment_sneakers = [
        "For basketball",
        "For running",
        "For boxing",
        "For volleyball",
        "For gym ",
        "For tennis",
    ]
    return random.choice(list_name_assignment_sneakers)


def get_random_color():
    list_color_sneakers = ["Blue", "Green", "Red", "White", "Yellow", "Pink", "Brown"]
    return random.choice(list_color_sneakers)


def get_random_size():
    size = [size for size in range(37, 48)]
    return random.choice(size)


def get_random_categories_sneakers():
    list_categories_sneakers = [
        "Sporty sneakers",
        "Trendy sneakers",
        "Fashion sneakers",
        "Casual sneakers",
        "Athletic Footwear",
        "Running Shoes",
    ]
    return random.choice(list_categories_sneakers)
