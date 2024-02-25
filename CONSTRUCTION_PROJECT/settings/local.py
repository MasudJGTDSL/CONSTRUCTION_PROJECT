from .base import *

if int(config["MIDDLEWARE"]) == 1:
    MIDDLEWARE += ["CONSTRUCTION_PROJECT.settings.middleware.masud_for_sql_middleware"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "ConstructionProject.sqlite3",
    }
}

if int(config["LOGGING"]) == 1:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "level": "DEBUG",  # Set this to the desired log level.
                "class": "logging.FileHandler",
                "filename": "django.log",  # Provide the path to the log file.
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": "DEBUG",  # Set this to the desired log level.
                "propagate": True,
            },
        },
        # "builtins": [
        #     "fdr.fdr_tag",
        # ],
    }
