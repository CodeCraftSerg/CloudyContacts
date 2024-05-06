"""
Django settings for CloudyContacts project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
# DEBUG = False
# DEBUG = True

ALLOWED_HOSTS = [
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1",
    "0.0.0.0",
    "web-pzjikg8utavf.up-de-fra1-k8s-1.apps.run-on-seenode.com",
    "cloudy-contacts-grey-edede0fc.koyeb.app",
    "api.openweathermap.org",
    "ipgeolocation.abstractapi.com",
    "suspilne.media/sport",
    "suspilne.media",
    "suspilne.media/culture",
    "api.ipify.org",
]
# ALLOWED_HOSTS = os.getenv(
#     "DJANGO_ALLOWED_HOSTS",
#     "localhost,127.0.0.1,[::1]",
#     "cloudy-contacts-grey-40c607a6.koyeb.app",
# ).split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://web-pzjikg8utavf.up-de-fra1-k8s-1.apps.run-on-seenode.com",
    "https://cloudy-contacts-grey-edede0fc.koyeb.app/",
]
# CSRF_TRUSTED_ORIGINS = os.getenv(
#     ""
# ).split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app_main",
    "users",
    "app_contacts",
    "app_notes",
    "app_files",
    "app_news",
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
]

ROOT_URLCONF = "CloudyContacts.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "CloudyContacts.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# --- SQLite Database ---
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# --- PostgreSQL Database ---
# DATABASES = {
#     "default": {
#         "ENGINE": env("DB_ENGINE"),
#         "NAME": env("DB_NAME"),
#         "USER": env("DB_USER"),
#         "PASSWORD": env("DB_PASSWORD"),
#         "HOST": env("DB_HOST"),
#         "PORT": env("DB_PORT"),
#     }
# }

# --- koyeb Database ---
# DATABASES = {
#     "default": {
#         "ENGINE": env("KOYEB_ENGINE"),
#         "NAME": env("KOYEB_NAME"),
#         "USER": env("KOYEB_USER"),
#         "PASSWORD": env("KOYEB_PASSWORD"),
#         "HOST": env("KOYEB_HOST"),
#     }
# }

# --- ElephantSQL Database ---
DATABASES = {
    "default": {
        "ENGINE": env("ELEPHANT_ENGINE"),
        "NAME": env("ELEPHANT_DB_NAME_USER"),
        "USER": env("ELEPHANT_DB_NAME_USER"),
        "PASSWORD": env("ELEPHANT_PASSWORD"),
        "HOST": env("ELEPHANT_HOST"),
        "PORT": env("ELEPHANT_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = "/users/signin"
LOGIN_REDIRECT_URL = "/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_STARTTLS = False
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")


CLOUDINARY_STORAGE = {
    "CLOUD_NAME": env("CLOUDINARY_NAME"),
    "API_KEY": env("CLOUDINARY_API_KEY"),
    "API_SECRET": env("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.RawMediaCloudinaryStorage"
