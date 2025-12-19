"""
Django settings for boutique_ado project.
"""

from pathlib import Path


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------

SECRET_KEY = "django-insecure-bf_nx7m0sd(kbofoqv1g*ba))$ux)2(ju#mr-kr5#21@5iql_d"

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]


# ------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Local apps
    "home",
    "products",
    "bag",
    "checkout",
]

INSTALLED_APPS = DJANGO_APPS


# ------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ------------------------------------------------------------
# URLS / WSGI
# ------------------------------------------------------------

ROOT_URLCONF = "boutique_ado.urls"
WSGI_APPLICATION = "boutique_ado.wsgi.application"


# ------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "templates" / "allauth",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "bag.contexts.bag_contents",
            ],
        },
    },
]


# ------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ------------------------------------------------------------
# STATIC FILES (CSS, JS, IMAGES)
# ------------------------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# ------------------------------------------------------------
# MEDIA FILES (USER UPLOADS)
# ------------------------------------------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ------------------------------------------------------------
# DEFAULTS
# ------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------
# SITES / AUTHENTICATION
# ------------------------------------------------------------

SITE_ID = 1


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# ------------------------------------------------------------
# EMAIL (DEV)
# ------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ------------------------------------------------------------
# DJANGO-ALLAUTH SETTINGS
# ------------------------------------------------------------

ACCOUNT_LOGIN_METHODS = ("username", "email")


ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]


ACCOUNT_EMAIL_VERIFICATION = "mandatory"


ACCOUNT_USERNAME_MIN_LENGTH = 4


# ------------------------------------------------------------
# LOGIN / LOGOUT REDIRECTS
# ------------------------------------------------------------

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"


# ------------------------------------------------------------
# SHOP SETTINGS
# ------------------------------------------------------------

FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10
