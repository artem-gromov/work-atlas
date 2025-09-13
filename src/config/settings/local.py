from .base import *  # noqa: F401,F403
from .base import BASE_DIR

DEBUG = True
TENANT_DEFAULT_DOMAIN_SUFFIX = ".app.local"
ALLOWED_HOSTS = ["*"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
