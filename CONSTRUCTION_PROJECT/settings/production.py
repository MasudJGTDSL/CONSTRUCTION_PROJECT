from .base import *


if config["GUNICORN"] != "None":
    INSTALLED_APPS += config["GUNICORN"].split(" ")

# INSTALLED_APPS += [
#     "gunicorn",
# ]

# ALLOWED_HOSTS = [
#     "192.168.0.101",
#     "118.179.146.204",
#     "aerosky.mahimsoft.com.bd",
#     # "mahimsoft.com.bd",
#     # "18.143.78.181",
# ]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "ConstructionProject_Production.sqlite3",
    }
}
