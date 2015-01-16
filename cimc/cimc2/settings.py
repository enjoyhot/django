"""
Django settings for cimc2 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kz#9om-o$*n#=d8fc(ipv6%h1co5wv7hpsk)yts+mv@w_4c!l&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',	
   # 'mongoengine.django.mongo_auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'pagination',
    'hello',
    'servers',
    'instance',
    'create',
    'gunicorn',
)

# WebVirtMgr settings
#SECRET_KEY = None
#LOCAL_PATH = None
TIME_JS_REFRESH = 2000
WS_PORT = 6080
WS_HOST = '0.0.0.0'

USE_L10N = True

USE_TZ = True

# to load the internationalization machinery.
USE_I18N = True

LIBVIRT_KEEPALIVE_INTERVAL = 5
LIBVIRT_KEEPALIVE_COUNT    = 5

#try:
#    from local.local_settings import *  # noqa
#except ImportError:
#    logging.warning("No local_settings file found.")

# Ensure that we always have a SECRET_KEY set, even when no local_settings.py
# file is present.
# THIS IS A BACKPORT FROM HORIZON https://github.com/openstack/horizon
#if not SECRET_KEY:
#   if not LOCAL_PATH:
#        LOCAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                  'local')

#    from webvirtmgr.utils import secret_key

#    SECRET_KEY = secret_key.generate_or_read_from_file(os.path.join(LOCAL_PATH,
#                                                                    '.secret_key_store'))

# list taken from http://qemu.weilnetz.de/qemu-doc.html#sec_005finvocation
QEMU_KEYMAPS = ['ar', 'da', 'de', 'de-ch', 'en-gb', 'en-us', 'es', 'et', 'fi',
                'fo', 'fr', 'fr-be', 'fr-ca', 'fr-ch', 'hr', 'hu', 'is', 'it',
                'ja', 'lt', 'lv', 'mk', 'nl', 'nl-be', 'no', 'pl', 'pt',
                'pt-br', 'ru', 'sl', 'sv', 'th', 'tr']
#LOCALE_PATHS = (
#    os.path.join(os.path.dirname(__file__), '..', 'locale'),
#)

TEMPLATE_CONTEXT_PROCESSORS=(
    #'django.core.auth.context_processors.auth',
    'django.contrib.auth.context_processors.auth',
    #'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    #'django.core.context_processors.media',
    #'django.core.context_processors.static',
    #'django.core.context_processors.request',
)

#MONGOENGINE_USER_DOCUMENT='mongoengine.django.auth.User'
SESSION_ENGINE='mongoengine.django.sessions'
#SESSION_SERIALIZER='mongoengine.django.sessions.BSONSerializer'
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'pagination.middleware.PaginationMiddleware',
)

AUTHENTICATION_BACKENDS=(
    'mongoengine.django.auth.MongoEngineBackend',
)

ROOT_URLCONF = 'cimc2.urls'

WSGI_APPLICATION = 'cimc2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
  #  'default': {
 #       'ENGINE': 'django.db.backends.dummy',
  #      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), '..', 'webvirtmgr.sqlite3'),
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MIDIA_ROOT=os.path.join(BASE_DIR,'media')

MIDIA_URL='/media/'

#from mongoengine import connect
#connect('cimc_user')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
#INSTALLED_APPS += [django.contrib.staticfiles,]
#STATICFILES_FINDERS=(
#	'django.contrib.staticfiles.finders.FileSystemFinder',
#	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#)

STATICFILES_DIRS = (
	 os.path.join(os.path.dirname(__file__),'static'),
)
#STATIC_ROOT = os.path.join(os.path.dirname(__file__),'..', 'static')
#STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..','static')
STATIC_URL = '/static/'
#STATIC_URL = os.path.join(os.path.dirname(__file__), '..','static/')
#ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'


TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates'),)

LOGIN_URL='/cimc/login'
#STATIC_ROOT='/home/gugugujiawei/DjangoServer/cimc2/hello/static/'
