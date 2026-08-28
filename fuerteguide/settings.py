from pathlib import Path
import os
import sys

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / ".vendor"))
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-fuerteguide-key")
DEBUG = os.environ.get("DEBUG", "True").lower() in {"1", "true", "yes"}
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
ALLOWED_HOSTS.append("healthcheck.railway.app")
# A leading dot allows both Railway's generated root host and its subdomains.
ALLOWED_HOSTS.append(".up.railway.app")
RAILWAY_PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]
if RAILWAY_PUBLIC_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_PUBLIC_DOMAIN}")
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "directory",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware", "django.middleware.common.CommonMiddleware",
    "fuerteguide.translation.SiteTranslationMiddleware", "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "fuerteguide.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True, "OPTIONS": {"context_processors": [
        "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages", "fuerteguide.context_processors.language_navigation",
    ]},
}]
WSGI_APPLICATION = "fuerteguide.wsgi.application"
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
if DATABASE_URL:
    import dj_database_url
    DATABASES = {"default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=not DEBUG,
    )}
elif not DEBUG:
    raise ImproperlyConfigured(
        "DATABASE_URL is required when DEBUG=False. Connect the Railway PostgreSQL "
        "service with DATABASE_URL=${{Postgres.DATABASE_URL}}; SQLite on Railway is ephemeral."
    )
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en-gb"
LANGUAGES = [("en", "English"), ("es", "Español"), ("it", "Italiano")]
TIME_ZONE = "Atlantic/Canary"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
RAILWAY_VOLUME_MOUNT_PATH = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "").strip()
# Database records live in PostgreSQL. User-uploaded files live on the attached
# Railway volume so their paths and the files they reference both survive deploys.
MEDIA_ROOT = (
    Path(RAILWAY_VOLUME_MOUNT_PATH) / "media"
    if RAILWAY_VOLUME_MOUNT_PATH
    else BASE_DIR / "media"
)
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", str(not DEBUG)).lower() in {"1", "true", "yes"}
SECURE_REDIRECT_EXEMPT = [r"^health/$"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Public Google Calendar shown on the Events page. Google Calendar IDs are safe
# to expose only when the calendar itself has been made public.
GOOGLE_CALENDAR_ID = os.environ.get("GOOGLE_CALENDAR_ID", "").strip()
GOOGLE_CALENDAR_TIME_ZONE = os.environ.get("GOOGLE_CALENDAR_TIME_ZONE", "Atlantic/Canary").strip()
