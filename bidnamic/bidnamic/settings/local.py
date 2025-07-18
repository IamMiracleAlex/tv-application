from .base import *

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-ncqfv4_t#v5slu7@trb1m8)k-y5wa5yh7uyvuhcs(6(7#*7lis"
)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if os.environ.get("USE_DOCKER") == "Yes":
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE"),
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
