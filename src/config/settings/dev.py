from config.settings.base import *  # NOQA

SECRET_KEY = "django-insecure-p_w@c@sfst@&tr7@c_9nqw619g__taezdm7xlc=g#94(=eyxu#"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += []  # NOQA

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}

STATIC_URL = "static/"
