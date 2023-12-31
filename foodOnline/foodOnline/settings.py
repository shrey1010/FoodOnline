'templates'"""
Django settings for foodOnline project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',default = False,cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "accounts",
    "vendor",
    "menu",
    "marketplace", 
    "customers", 
    "orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'orders.request_object.RequestObjectMiddleware'   # custom request object middleware
]

ROOT_URLCONF = "foodOnline.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.get_vendor",
                "accounts.context_processors.get_user_profile",
                "accounts.context_processors.get_google_api",
                "accounts.context_processors.get_paypal_id",
                "marketplace.context_processors.get_cart_counter",
                "marketplace.context_processors.get_cart_ammount",
                
            ],
        },
    },
]

WSGI_APPLICATION = "foodOnline.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DATABASE_ENGINE"),
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
    }
}

AUTH_USER_MODEL = 'accounts.User'  

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    'foodOnline/static'
]

# media file configurations
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR:'danger',
}

#Email configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT',cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


# Google api configuration
GOOGLE_API_KEY = config('GOOGLE_API_KEY')


import os 
# for spatial data with virtual environment 
# os.environ['PATH'] = os.path.join(BASE_DIR, 'envLibsite-packagesosgeo') + ';' + os.environ['PATH']
# os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'envLibsite-packagesosgeodataproj') + ';' + os.environ['PATH']
# GDAL_LIBRARY_PATH = os.path.join(BASE_DIR, 'envLibsite-packagesosgeogdal304.dll') 


# for spatial data without virtual environment 
DIR = r'C:\Users\shrey\AppData\Local\Programs\Python\Python311'

# Update PATH
os.environ['PATH'] = os.path.join(DIR, 'Lib', 'site-packages', 'osgeo') + ';' + os.environ['PATH']

# Update PROJ_LIB
os.environ['PROJ_LIB'] = os.path.join(DIR, 'Lib', 'site-packages', 'osgeodataproj') + ';' + os.environ.get('PROJ_LIB', '')

# Set GDAL_LIBRARY_PATH
GDAL_LIBRARY_PATH = os.path.join(DIR, 'Lib', 'site-packages', 'osgeo', 'gdal304.dll') 

# Now, you can use GDAL_LIBRARY_PATH wherever you need it in your code.


# paypal 
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')
RAZORPAY_CLIENT_ID = config('RAZORPAY_CLIENT_ID')
RAZORPAY_CLIENT_SECRET = config('RAZORPAY_CLIENT_SECRET')

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
