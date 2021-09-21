"""Settings that need to be set in order to run the tests."""
import os

from django.urls import reverse_lazy

DEBUG = True

SITE_ID = 1

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


ROOT_URLCONF = "hijack.tests.test_app.urls"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(APP_ROOT, "../app_static")
MEDIA_ROOT = os.path.join(APP_ROOT, "../app_media")
STATICFILES_DIRS = (os.path.join(APP_ROOT, "static"),)

NOSE_ARGS = []

TEMPLATE_DIRS = (os.path.join(APP_ROOT, "tests/test_app/templates"),)

PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.SHA1PasswordHasher",
    "django.contrib.auth.hashers.MD5PasswordHasher",
    "django.contrib.auth.hashers.CryptPasswordHasher",
)

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "hijack.middleware.HijackUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

EXTERNAL_APPS = [
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
]

INTERNAL_APPS = [
    "hijack",
    "hijack.contrib.admin",
    "hijack.tests.test_app",
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

SECRET_KEY = "foobar"

LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_TZ = True

LOGOUT_REDIRECT_URL = reverse_lazy("bye-bye")

AUTH_USER_MODEL = "test_app.CustomUser"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"
