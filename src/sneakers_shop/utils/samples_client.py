from django.contrib.auth import get_user_model


def exemple_client(first_name: str, last_name: str, email: str, **kwargs):
    default = {"first_name": first_name, "last_name": last_name, "email": email, "is_staff": True, "is_active": True}
    default.update(kwargs)
    default["first_name"] = first_name
    default["last_name"] = last_name
    return get_user_model().objects.create_user(**default)
