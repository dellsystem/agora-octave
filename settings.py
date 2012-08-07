# Django settings for agora project.
# -*- coding: utf-8 -*-

import sys

import django.conf.global_settings as DEFAULT_SETTINGS

# Read some settings from config file
from ConfigParser import ConfigParser
config = ConfigParser()

#This makes options in the config case-sensitive
config.optionxform = str

if not config.read('agora.conf'):
    print >> sys.stderr, '''
ERROR: No config file found!
    You probably should copy agora-example.conf to agora.conf
''';
    exit(1)

try:
    DEBUG = (config.get('debug', 'debug').lower() == 'yes')
except:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

try:
    ADMINS = tuple(config.items('admins'))
except:
    ADMINS = ()

MANAGERS = ADMINS

try:
    database = dict(config.items('db'))
except:
    database = {'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'agora'}

DATABASES = {
    'default': database
}

try:
    tz = config.get('env','timezone')
except:
    tz = 'America/Mexico_City'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = tz

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

try:
    secret_key = config.get('security', 'secret_key')
except:
    secret_key = 'l0ng-str1ng-no-one-w1ll-gue55-with-numb3rs-4nd-letters'

# Make this unique, and don't share it with anybody.
SECRET_KEY = secret_key

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Agora-specific middleware
    'agora.middleware.http.Http403Middleware',
)

ROOT_URLCONF = 'agora.urls'

TEMPLATE_DIRS = (
    # Probably should make this an absolute path on an actual
    # installation, but on a debug setup relative paths work fine.
    "templates",
)

ACCOUNT_ACTIVATION_DAYS = 1

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admindocs',
    'django.contrib.admin',
#	'django.contrib.comments',

    # Third-party apps
    'registration',
#	'threadedcomments',

    # Agora apps
    'agora.apps.profile',
    'agora.apps.snippet',
    'agora.apps.bundle',
    'agora.apps.free_license',
    'agora.apps.mptt',
)

COMMENTS_APP = 'threadedcomments'

LOGIN_REDIRECT_URL='/'
AUTH_PROFILE_MODULE = 'profile.Profile'
