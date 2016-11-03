import os
import platform
import socket

from unipath import Path

from edc_map.classes import site_mappers
from .installed_apps import DJANGO_APPS, THIRD_PARTY_APPS, EDC_APPS, LIS_APPS, LOCAL_APPS
from .bcpp_settings import MAX_HOUSEHOLDS_PER_PLOT
from .databases import NETBOOK_MYSQL
from .device import CURRENT_COMMUNITY, SITE_CODE, DEVICE_ID
from .mail_settings import (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
                            EMAIL_HOST_PASSWORD, EMAIL_USE_TLS)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (('erikvw', 'ew@2789@gmail.com'),)

# PATHS
DIRNAME = os.path.dirname(os.path.abspath(__file__))  # needed??
SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(3)  # e.g. /home/django/source
EDC_DIR = SOURCE_ROOT.child('edc_project').child('edc')  # e.g. /home/django/source/edc_project/edc
TEMPLATE_DIRS = (
    EDC_DIR.child('templates'),
)
PROJECT_ROOT = Path(__file__).ancestor(3)  # e.g. /home/django/source/bhp066_project
PROJECT_DIR = Path(__file__).ancestor(2)  # e.g. /home/django/source/hp066_project/bhp066
ETC_DIR = PROJECT_DIR.child('config').child('etc')  # for production this should be /etc/edc
MEDIA_ROOT = PROJECT_DIR.child('media')
STATIC_ROOT = PROJECT_DIR.child('static')
FIXTURE_DIRS = (
    PROJECT_DIR.child('apps', 'bcpp', 'fixtures'),
)
STATICFILES_DIRS = ()
CONFIG_DIR = PROJECT_DIR.child('config')
MAP_DIR = STATIC_ROOT.child('img')

# edc.crytpo_fields encryption keys
if socket.gethostname() == 'mac.local':
    KEY_PATH = '/Volumes/bhp066/live_keys'  # DONT DELETE ME!!, just comment out
elif socket.gethostname() == 'ckgathi':
    KEY_PATH = '/Users/ckgathi/source/bhp066_project/bhp066/keys'
else:
    KEY_PATH = '/Users/sirone/Documents/workspace/git_projects/bhp066_git/bhp066/keys'
MANAGERS = ADMINS

# DATABASES
CONN_MAX_AGE = 15
DATABASES = NETBOOK_MYSQL

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', 'bhpserver']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Gaborone'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# langauage setting

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

ugettext = lambda s: s  # does this do anything?

LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    PROJECT_DIR.child('locale'),
)

LANGUAGE_CODE = 'en'

SITE_ID = 1

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL that handles the static files served from STATIC_ROOT.
STATIC_URL = '/static/'

# A list of locations of additional static files
STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

# Make this unique, and don't share it with anybody.
with open(os.path.join(ETC_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
     'django.template.loaders.filesystem.Loader',
     'django.template.loaders.app_directories.Loader',
     'django.template.loaders.eggs.Loader',
     )),
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.request",
                               "django.contrib.messages.context_processors.messages",
                               )

ROOT_URLCONF = 'config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'config.wsgi.application'

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + EDC_APPS + LIS_APPS + LOCAL_APPS  # + ('django_nose', )

# django
SESSION_COOKIE_AGE = 10000
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# django email settings
EMAIL_HOST = EMAIL_HOST
EMAIL_PORT = EMAIL_PORT
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = EMAIL_USE_TLS
# EMAIL_AFTER_CONSUME = False

# django auth
AUTH_PROFILE_MODULE = "bhp_userprofile.userprofile"

# general
APP_NAME = 'bcpp'
PROJECT_NUMBER = 'BHP066'
PROJECT_IDENTIFIER_PREFIX = '066'
PROJECT_IDENTIFIER_MODULUS = 7
PROTOCOL_REVISION = 'V1.0 24 September 2013'
INSTITUTION = 'Botswana-Harvard AIDS Institute Partnership'

# admin overrides
LOGIN_URL = '/{app_name}/login/'.format(app_name=APP_NAME)
LOGIN_REDIRECT_URL = '/{app_name}/'.format(app_name=APP_NAME)
LOGOUT_URL = '/{app_name}/logout/'.format(app_name=APP_NAME)

# south
SOUTH_LOGGING_FILE = os.path.join(os.path.dirname(__file__), "south.log")
SOUTH_LOGGING_ON = True

# dajax
DAJAXICE_MEDIA_PREFIX = "dajaxice"

# edc.subject.registered_subject
SUBJECT_APP_LIST = ['bcpp_subject', 'bcpp_clinic']
SUBJECT_TYPES = ['subject']
MAX_SUBJECTS = {'subject': 9999}

# edc.device.dispatch
DISPATCH_APP_LABELS = ['bcpp_subject', 'bcpp_household', 'bcpp_household_member',
                       'bcpp_lab', 'bcpp_survey']

# edc.crypto_fields
IS_SECURE_DEVICE = False
MAY_CREATE_NEW_KEYS = True
FIELD_MAX_LENGTH = 'migration'

# edc.map
SITE_CODE = SITE_CODE
CURRENT_COMMUNITY = CURRENT_COMMUNITY
CURRENT_COMMUNITY_CHECK = True  # turn this to true on the netbooks to make a community check is run on netbooks
CURRENT_MAPPER = CURRENT_COMMUNITY
GPS_FILE_NAME = '/Volumes/GARMIN/GPX/temp.gpx'
GPS_DEVICE = '/Volumes/GARMIN/'
GPX_TEMPLATE = os.path.join(STATIC_ROOT, 'gpx/template.gpx')
VERIFY_GPS = False

# edc.lab
LAB_SECTION = 'bcpp_lab'
LAB_LOCK_NAME = 'BHP066'
LABDB = 'bhplab'
REFERENCE_RANGE_LIST = 'BHPLAB_NORMAL_RANGES_201005'
GRADING_LIST = 'DAIDS_2004'
if platform.system() == 'Darwin':
    LAB_IMPORT_DMIS_DATA_SOURCE = ('DRIVER=/usr/local/lib/libtdsodbc.so;SERVER=192.168.1.141;'
                                   'PORT=1433;UID=sa;PWD=cc3721b;DATABASE=BHPLAB')
else:
    LAB_IMPORT_DMIS_DATA_SOURCE = ('DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;'
                                   'DATABASE=BHPLAB')
# edc.subject.consent
SUBJECT_IDENTIFIER_UNIQUE_ON_CONSENT = False  # set to False so that the constraint can be expanded to subject_identifier + survey

#  edc.device.device
DEVICE_ID = '86'
SERVER_DEVICE_ID_LIST = [91, 92, 93, 94, 95, 96, 97, 99]
MIDDLEMAN_DEVICE_ID_LIST = [98]
if str(DEVICE_ID) == '98':
    PROJECT_TITLE = 'MIDDLEMAN: Botswana Combination Prevention Project'
elif str(DEVICE_ID) == '99':
    PROJECT_TITLE = 'SERVER: Botswana Combination Prevention Project'
    BYPASS_HOUSEHOLD_LOG = True
    COMMUNITY = 'BHP'
elif str(DEVICE_ID) in map(str, range(91, 97)):
    PROJECT_TITLE = 'COMMUNITY: Botswana Combination Prevention Project'
    BYPASS_HOUSEHOLD_LOG = True
else:
    PROJECT_TITLE = 'FIELD' + DEVICE_ID + ': Botswana Combination Prevention Project'
PROJECT_TITLE = PROJECT_TITLE + ' | ' + SITE_CODE + ' | ' + CURRENT_COMMUNITY

# edc.device.inspector (middleman)
MIDDLE_MAN_LIST = ['resourcemac-bhp066']

# edc.device.sync
ALLOW_MODEL_SERIALIZATION = True

# bcpp_settings
BHS_START_DATE = site_mappers.get_mapper(site_mappers.current_community).bhs_start_date
BHS_END_DATE = site_mappers.get_mapper(site_mappers.current_community).bhs_end_date
BHS_FULL_ENROLLMENT_DATE = site_mappers.get_mapper(site_mappers.current_community).bhs_full_enrollment_date
SMC_START_DATE = site_mappers.get_mapper(site_mappers.current_community).smc_start_date
MAX_HOUSEHOLDS_PER_PLOT = MAX_HOUSEHOLDS_PER_PLOT
LABEL_PRINTER_MAKE_AND_MODEL = ['Zebra ZPL Label Printer']
