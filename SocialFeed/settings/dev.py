from SocialFeed.settings.base import *
import os

DEBUG = True

ALLOWED_HOSTS = ["herokuapp.com", "127.0.0.1"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "SocialFeedDB",
        "USER": "postgres",
        "PASSWORD": os.environ.get("PGPSW"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
