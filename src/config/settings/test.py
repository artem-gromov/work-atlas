from .base import *  # noqa: F401,F403
from .base import BASE_DIR

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}

SPATIALITE_LIBRARY_PATH = env("SPATIALITE_LIBRARY_PATH", default="mod_spatialite")
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Simplify configuration for the lightweight spatialite test setup
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

SHARED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tenancy",
    "accounts",
]

TENANT_APPS = ["profiles", "companies"]

INSTALLED_APPS = ["django.contrib.admin"] + SHARED_APPS + TENANT_APPS

DATABASE_ROUTERS = []
TENANT_MODEL = "tenancy.Tenant"
TENANT_DOMAIN_MODEL = "tenancy.Tenant"
