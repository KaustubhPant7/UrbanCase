from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())
ALLOWED_HOSTS += [".railway.app", ".up.railway.app", ".vercel.app"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "storages",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "core",
    "products",
    "orders",
    "users",
    "wishlist",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_context",
                "wishlist.context_processors.wishlist_count",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ── Database ──────────────────────────────────────────────────────────
if config("USE_POSTGRES", default=False, cast=bool):
    DATABASES = {
        "default": {
            "ENGINE":       "django.db.backends.postgresql",
            "NAME":         config("POSTGRES_DB",       default="railway"),
            "USER":         config("POSTGRES_USER",     default="postgres"),
            "PASSWORD":     config("POSTGRES_PASSWORD", default=""),
            "HOST":         config("DB_HOST",           default="localhost"),
            "PORT":         config("DB_PORT",           default="5432"),
            "CONN_MAX_AGE": config("DB_CONN_MAX_AGE",  default=0, cast=int),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME":   BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ── Static files (served by WhiteNoise) ───────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
    if not DEBUG
    else "django.contrib.staticfiles.storage.StaticFilesStorage"
)

# ── Media files ───────────────────────────────────────────────────────
# In production: stored on Cloudflare R2 (S3-compatible, free tier).
# In development: stored locally.
_USE_S3 = config("USE_S3", default=False, cast=bool)

if _USE_S3:
    # Cloudflare R2 / AWS S3 settings
    AWS_ACCESS_KEY_ID       = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY   = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="urbancase-media")
    AWS_S3_REGION_NAME      = config("AWS_S3_REGION_NAME",      default="auto")
    AWS_S3_ENDPOINT_URL     = config("AWS_S3_ENDPOINT_URL",     default="")
    AWS_S3_CUSTOM_DOMAIN    = config("AWS_S3_CUSTOM_DOMAIN",    default="")
    AWS_DEFAULT_ACL         = "public-read"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_QUERYSTRING_AUTH    = False

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    else:
        MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"
else:
    MEDIA_URL  = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── django-allauth ────────────────────────────────────────────────────
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": config("GOOGLE_CLIENT_ID",     default=""),
            "secret":    config("GOOGLE_CLIENT_SECRET", default=""),
            "key": "",
        },
    }
}

LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "/"

# ── Email ──────────────────────────────────────────────────────────────
EMAIL_BACKEND       = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST          = config("EMAIL_HOST",          default="smtp.gmail.com")
EMAIL_PORT          = config("EMAIL_PORT",          default=587, cast=int)
EMAIL_USE_TLS       = config("EMAIL_USE_TLS",       default=True, cast=bool)
EMAIL_HOST_USER     = config("EMAIL_HOST_USER",     default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL  = config("DEFAULT_FROM_EMAIL",  default="UrbanCase <noreply@urbancase.com>")

# ── Production security ────────────────────────────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER        = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT            = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
    SESSION_COOKIE_SECURE          = True
    CSRF_COOKIE_SECURE             = True
    SECURE_HSTS_SECONDS            = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD            = False
    SECURE_CONTENT_TYPE_NOSNIFF    = True
    X_FRAME_OPTIONS                = "DENY"
