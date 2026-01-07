import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "appdb"),
        "USER": os.getenv("POSTGRES_USER", "appuser"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "apppass"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Atlantic/Canary'
USE_I18N = True
USE_TZ = True
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host]

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'ns0.ovh.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = "contacto@dsegur.com"
EMAIL_HOST_PASSWORD = "t5C7rjVCh!Ux"
EMAIL_FROM_DEFAULT = 'contacto@dsegur.com'