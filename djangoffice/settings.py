# Django settings for djangoffice project.

import os
from pathlib import Path
from environs import Env
env = Env()
env.read_env()  # read .env file, if it exists

DIRNAME = os.path.dirname(__file__)
BASE_DIR = Path(__file__).resolve().parent

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Belfast'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(DIRNAME, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')   #BASE_DIR / 'static'  # should match with template staticfiles
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'djangoffice/static'), ]    

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4z-(+=l(wkd)1aj+wn)(r%6z)*s*thfbi9u%1&uu_w$ids#ww='



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoffice.urls'

# Authentication settings
AUTH_PROFILE_MODULE = 'djangoffice.UserProfile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/jobs/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # project level templates
        'DIRS': [os.path.join(BASE_DIR, 'djangoffice/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                # 'django.template.context_processors.csrf',      # security enhance TODO
                'django.contrib.messages.context_processors.messages',
                'djangoffice.context_processors.app_constants',
            ],
            'libraries' : {
                'staticfiles': 'django.templatetags.static', 
            }            
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'dbsettings',

    'djangoffice',

    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',    #debugging tool, jupyter

]

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

# Application constants
APPLICATION_NAME = 'Djangoffice&copy;'
APPLICATION_VERSION = '1.5'

# Number of items on each when paginating
ITEMS_PER_PAGE = 15

# Admininstration Job id
ADMIN_JOB_ID = 1

# Company Details
COMPANY_NAME = 'Generitech'
COMPANY_ADDRESS = {
    'street_line_1': '123 Fake St.',
    'street_line_2': 'Fiction Road',
    'town_city': 'Madeupstown',
    'postcode': 'BT12 34S6',
}
COMPANY_CONTACT = {
    'phone_number': '028 1234 5678',
    'fax_number': '028 1234 5679',
    'email': 'info@generitech.co.uk',
}
COMPANY_URL = 'http://www.generitech.co.uk'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Load local settings if present - place setting modifications in a
# local_settings module rather than editing this file, which should
# contain development settings.
try:
    from djangoffice.settings import *
except ImportError:
    pass
