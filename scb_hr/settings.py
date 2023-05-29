from pathlib import Path
import environ

from celery.schedules import crontab
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
Env.read_env(str(BASE_DIR / ".env"))

SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG", True)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django_bootstrap5",
    'django_filters',

    "vacancy.apps.VacancyConfig",
    "inspector.apps.InspectorConfig",
    "candidate.apps.CandidateConfig",
    "archive.apps.ArchiveConfig",
    "position.apps.PositionConfig",
    "account.apps.AccountConfig",
    "parsing.apps.ParsingConfig",
    "report.apps.ReportConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "scb_hr.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "scb_hr.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL", "sqlite:///db.sqlite3")}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = "H:i d/m/Y"

USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = env.str("MEDIA_ROOT", BASE_DIR / 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'account.CustomUser'

LOGIN_URL = '/account/accounts/login/'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND")
CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "scb_hr.celery.send_out_interview_reminders",
        "schedule": crontab(
            env.int("SEND_OUT_INTERVIEW_REMINDERS_MINUTE", 0),
            env.int("SEND_OUT_INTERVIEW_REMINDERS_HOUR", 0),
        ),
    },
}

CSRF_TRUSTED_ORIGINS = ["https://syntaxinvalid-scb.ddns.net"]

# Login, passwords, tokens and others

SUPERJOB_TOKEN = env.str("SUPERJOB_TOKEN")
SUPERJOB_PAGE_COUNT = env.int("SUPERJOB_PAGE_COUNT", 10)

EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.int("EMAIL_PORT")

BASE_URL = env.str("BASE_URL")

TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
