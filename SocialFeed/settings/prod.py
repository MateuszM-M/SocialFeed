from SocialFeed.settings.base import *
import os

DEBUG = False

ALLOWED_HOSTS = ["hello-social-feed.herokuapp.com", "127.0.0.1", "herokuapp.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "SocialFeedDB",
        "USER": "SFDB",
        "PASSWORD": os.environ.get("SOCIALFEED_DB_PASSWORD"),
        "HOST": "socialfeeddb.cijqn9skmpbv.eu-central-1.rds.amazonaws.com",
        "PORT": "5432",
    }
}

AWS_ACCESS_KEY_ID = os.environ.get("SOCIALFEED_S3_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("SOCIALFEED_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "hello-social-feed"

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_HOST = "s3.us-east-2.amazonaws.com"
AWS_S3_REGION_NAME = "us-east-2"

AWS_QUERYSTRING_AUTH = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
