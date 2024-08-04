from config.settings.base import *  # NOQA

SECRET_KEY = os.environ.get("SECRET_KEY")  # NOQA F405

DEBUG = False


ALLOWED_HOSTS = [
    "ec2-16-16-24-143.eu-north-1.compute.amazonaws.com", # NOQA
    "localhost",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static/"  # NOQA


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media/"  # NOQA
