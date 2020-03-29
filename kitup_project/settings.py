"""
Django settings for kitup_project project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# References the template directory in which the HTML files are held.
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# References the static files dir in which media and other files are held.
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# References the path to where media files will be uploaded by the users.
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+3_#$o94)7_bm-hbhp7bjgqtn_6a2599m-5##md04unlxn52l2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'

# Used by Django to find the paths to the static files. Because we're using static
# local files, this denotes the root directory of the static files.
STATICFILES_DIRS = [STATIC_DIR,]

# Used bu django to set up media file hosting.
# The '/' ensures that the root of the URL '/media/' is separate
# from the file names that are being uploaded.

# MEDIA_ROOT informs django where to look for the media files in the file
# system.
MEDIA_ROOT = MEDIA_DIR

# MEDIA_URL informs django the URL that should be served.
MEDIA_URL = '/media/'

# The templates that are to be utilised by crispy_froms library.
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Whether or not the date / time pickers should be localized.
TEMPUS_DOMINUS_LOCALIZE = True

# Required by django-address, attempts to find the exact whereabouts.
GOOGLE_API_KEY = 'AIzaSyDIj0SneZsfoYp6GTn4cCB5m2Vw7igB9Sg'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap4',
    'crispy_forms',
    'tempus_dominus',

    'social_django',

    'kitup'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kitup_project.urls'


# 'django.template.context_processors.media' enables RequestContext to contain a variable MEDIA_URL

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'kitup_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Social media authentication backends
AUTHENTICATION_BACKENDS = [
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


FACEBOOK_APP_KEY = 675634196622515
FACEBOOK_APP_SECRET = "2b4dd50dfedbb56ad5719c09b30"

SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_APP_KEY        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_APP_SECRET  # App Secret