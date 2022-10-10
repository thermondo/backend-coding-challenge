import os
from django.conf import settings

from .settings import *

# Get main database/third party service configurations from os environment to the app
DATABASE_ENGINE = os.environ.get(
    "DATABASE_ENGINE", "django.db.backends.postgresql_psycopg2"
)
DATABASE_HOST = os.environ.get("DATABASE_HOST", "127.0.0.1")
DATABASE_PORT = os.environ.get("DATABASE_PORT", 5432)
DATABASE_NAME = os.environ.get("DATABASE_NAME", "thermondo_db")
DATABASE_USER = os.environ.get("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres_pass")

# Database
DATABASES = {
    "default": {
        "ENGINE": DATABASE_ENGINE,
        "NAME": DATABASE_NAME,
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": DATABASE_HOST,
        "PORT": DATABASE_PORT,
        "OPTIONS": {
            "connect_timeout": os.environ.get("DATABASE_CONNECTION_TIMEOUT", 5),
        },
    }
}

INSTALLED_APPS = settings.INSTALLED_APPS + ["django_extensions"]
