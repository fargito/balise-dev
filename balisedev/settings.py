"""
Django settings for balisedev project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import base64

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '1rq4niqp$a8r_&k!j$4(24!9tk!xyqm0hni8wv(l55*%d#6g+d'

keyfile = os.path.join(BASE_DIR, "secret.key")
if not os.path.exists(keyfile):
    with open(keyfile, "wb") as f:
        f.write(base64.b64encode(os.urandom(47)))
with open(keyfile, "r") as f:
    SECRET_KEY = f.read().strip()


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'compta',
    'accounts',
    'binets',
    'backend',
    'imports',
    'vos',
    'subventions',
    'passations',
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

ROOT_URLCONF = 'balisedev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'balisedev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

if DEBUG:
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
  }
else:
  DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.mysql',
       'OPTIONS': {
           'read_default_file': os.path.join(BASE_DIR, 'my.cnf'),
       },
    }
 }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# authentification Frankiz
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)
CAS_SERVER_URL = "https://cas.binets.fr/"


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


if DEBUG:
    STATIC_URL = '/static/'
else:
    STATIC_URL = '/assets/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "assets/static/")
MEDIA_ROOT = os.path.join(BASE_DIR, "assets/media/")
MEDIA_URL = '/assets/media/'

DEFAULT_FROM_EMAIL = "projetbalise@binets.polytechnique.fr"
# voir https://portail.polytechnique.edu/dsi/eleves/mail-binets
SERVER_EMAIL = DEFAULT_FROM_EMAIL
ADMINS = [("Webmaster", DEFAULT_FROM_EMAIL)]





if DEBUG:
    LOGIN_URL = '/accounts/login'
else:
    LOGIN_URL = '/login'

    
LOGIN_REDIRECT_URL = '/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
