import os
import sys
import socket

from unipath import Path

from .config.installed_apps import DJANGO_APPS, THIRD_PARTY_APPS, EDC_APPS, LIS_APPS, LOCAL_APPS
from .config.bcpp_settings import (
    APP_NAME, PROJECT_NUMBER, PROJECT_IDENTIFIER_PREFIX, PROJECT_IDENTIFIER_MODULUS,
    PROTOCOL_REVISION, INSTITUTION, MAX_HOUSEHOLDS_PER_PLOT, CURRENT_SURVEY,
    LIMIT_EDIT_TO_CURRENT_SURVEY, LIMIT_EDIT_TO_CURRENT_COMMUNITY,
    FILTERED_DEFAULT_SEARCH, STUDY_OPEN_DATETIME)
from .config.databases import TESTING_MYSQL, PRODUCTION_MYSQL
from .config.device import (
    CURRENT_COMMUNITY, SITE_CODE, DEVICE_ID, ADMIN_EXCLUDE_DEFAULT_CODE, VERIFY_GPS,
    VERIFY_GPS_LOCATION, VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER)
from .config.lab import LAB_IMPORT_DMIS_DATA_SOURCE
from .config.mail_settings import (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS)
from .config.middleman import MIDDLE_MAN_LIST


DEBUG = True  # Note: should be False for collectstatic
TEMPLATE_DEBUG = DEBUG
ADMINS = (('erikvw', 'ew@2789@gmail.com'),
          ('mkewagamang', 'mkewagamang@bhp.org.bw'),
          ('opharatlhatlhe', 'opharatlhatlhe@bhp.org.bw'),
          ('ckgathi', 'ckgathi@bhp.org.bw'),)

APP_NAME = APP_NAME

# PATHS
DIRNAME = os.path.dirname(os.path.abspath(__file__))  # needed??
BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
GIT_DIR = BASE_DIR.ancestor(1)

SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(2)  # e.g. /home/django/source
PROJECT_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)  # e.g. /home/django/source/bcpp
PROJECT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))  # e.g. /home/django/source/bcpp/bhp066
APP_DIR = PROJECT_DIR.child('apps').child(APP_NAME)  # e.g. /home/django/source/bhp066_project/bhp066/apps/bcpp
ETC_DIR = PROJECT_DIR.child('config').child('etc')  # for production this should be /etc/edc
MEDIA_ROOT = PROJECT_DIR.child('media')
STATIC_ROOT = PROJECT_DIR.child('static')
FIXTURE_DIRS = (
    APP_DIR.child('fixtures'),
)
STATICFILES_DIRS = ()
CONFIG_DIR = PROJECT_DIR.child('config')
MAP_DIR = STATIC_ROOT.child('img')

DEVELOPER_HOSTS = [
    'mac2-2.local', 'ckgathi', 'one-2.local', 'One-2.local', 'tsetsiba', 'leslie']

# edc.crytpo_fields encryption keys
# developers should set by catching their hostname instead of setting explicitly
if socket.gethostname() == 'mac2.local':
    KEY_PATH = '/Volumes/bhp066/live_keys'  # DONT DELETE ME!!, just comment out
elif socket.gethostname() in DEVELOPER_HOSTS:
    KEY_PATH = os.path.join(SOURCE_ROOT, 'crypto_fields/test_keys')
elif 'test' in sys.argv:
    KEY_PATH = os.path.join(SOURCE_ROOT, 'crypto_fields/test_keys')
elif socket.gethostname() == 'ckgathi':
    KEY_PATH = '/Users/ckgathi/source/bcpp/bhp066/keys'
elif socket.gethostname() == 'one-2.local' or socket.gethostname() == 'One-2.local':
    KEY_PATH = '/Users/sirone/Documents/workspace/git_projects/bhp066_git/bhp066/keys'
elif socket.gethostname() == 'silverapple':
    KEY_PATH = '/Users/melissa/Documents/git/source/bhp066_project/bhp066/keys'
elif socket.gethostname() == 'tsetsiba':
    KEY_PATH = '/Users/tsetsiba/source/keys'
else:
    # KEY_PATH = PROJECT_DIR.child('keys')  # DONT DELETE ME!!, just comment out
    # KEY_PATH = '/Volumes/keys'  # DONT DELETE ME!!, just comment out
    KEY_PATH = os.path.join(BASE_DIR.ancestor(1), 'keys')

ADMINS_HOST = ['ckgathi', 'tsetsiba', 'One-2.local', 'mac2.local']

MANAGERS = ADMINS

# DATABASES
CONN_MAX_AGE = 15
testing_db_name = 'sqlite'
if 'test' in sys.argv:
    # make tests faster
    SOUTH_TESTS_MIGRATE = False
    DATABASES = TESTING_MYSQL
else:
    DATABASES = PRODUCTION_MYSQL

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }
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


def ugettext(s):
    return s  # does this do anything?

LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
    ('kck', 'Ikalanga'),
    ('hbs', 'Hambukushu'),
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

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(SOURCE_ROOT.child('edc-base').child('edc_base'), 'templates')
)

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

ROOT_URLCONF = 'bhp066.config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bhp066.config.wsgi.application'

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + EDC_APPS + LIS_APPS  # + ('django_nose', )

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
PROJECT_NUMBER = PROJECT_NUMBER
PROJECT_IDENTIFIER_PREFIX = PROJECT_IDENTIFIER_PREFIX
PROJECT_IDENTIFIER_MODULUS = PROJECT_IDENTIFIER_MODULUS
PROTOCOL_REVISION = PROTOCOL_REVISION
INSTITUTION = INSTITUTION

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
SUBJECT_TYPES = ['subject', 'clinic']
MAX_SUBJECTS = {'subject': 99999,
                'clinic': 99999}

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
CURRENT_SURVEY = CURRENT_SURVEY
CURRENT_COMMUNITY_CHECK = False  # turn this to true on the netbooks to make a community check is run on netbooks
CURRENT_MAPPER = CURRENT_COMMUNITY
GPS_FILE_NAME = '/Volumes/GARMIN/GPX/temp.gpx'
GPS_DEVICE = '/Volumes/GARMIN/'
GPX_TEMPLATE = os.path.join(STATIC_ROOT, 'gpx/template.gpx')
VERIFY_GPS = VERIFY_GPS

# edc.lab
LAB_SECTION = 'bcpp_lab'
LAB_LOCK_NAME = 'BHP066'
LABDB = 'bhplab'
REFERENCE_RANGE_LIST = 'BHPLAB_NORMAL_RANGES_201005'
GRADING_LIST = 'DAIDS_2004'

LAB_IMPORT_DMIS_DATA_SOURCE = LAB_IMPORT_DMIS_DATA_SOURCE

# edc.subject.consent
# set to False so that the constraint can be expanded to subject_identifier + survey
SUBJECT_IDENTIFIER_UNIQUE_ON_CONSENT = False

#  edc.device.device
DEVICE_ID = DEVICE_ID
SERVER_DEVICE_ID_LIST = [91, 92, 93, 94, 95, 96, 97, 99]
MIDDLEMAN_DEVICE_ID_LIST = [98]
if str(DEVICE_ID) == '98':
    PROJECT_TITLE = 'MIDDLEMAN: Botswana Combination Prevention Project'
elif str(DEVICE_ID) == '99':
    PROJECT_TITLE = 'SERVER: Botswana Combination Prevention Project'
    BYPASS_HOUSEHOLD_LOG = True
elif str(DEVICE_ID) in map(str, range(91, 97)):
    PROJECT_TITLE = 'COMMUNITY: Botswana Combination Prevention Project'
    BYPASS_HOUSEHOLD_LOG = True
else:
    PROJECT_TITLE = 'FIELD' + str(DEVICE_ID) + ': Botswana Combination Prevention Project'
    BYPASS_HOUSEHOLD_LOG = False
PROJECT_TITLE = PROJECT_TITLE + ' | ' + SITE_CODE + ' | ' + CURRENT_COMMUNITY
VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER = VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER
VERIFY_GPS_LOCATION = VERIFY_GPS_LOCATION

# edc.device.inspector (middleman)
MIDDLE_MAN_LIST = MIDDLE_MAN_LIST

# edc.device.sync
ALLOW_MODEL_SERIALIZATION = True

# bcpp_settings
MAX_HOUSEHOLDS_PER_PLOT = MAX_HOUSEHOLDS_PER_PLOT
LABEL_PRINTER_MAKE_AND_MODEL = ['Zebra ZPL Label Printer']

# block editing of forms if not related to household_structure of current survey
# and community. set in bcpp_settings
LIMIT_EDIT_TO_CURRENT_SURVEY = False if DEVICE_ID == '99' else LIMIT_EDIT_TO_CURRENT_SURVEY
LIMIT_EDIT_TO_CURRENT_COMMUNITY = False if DEVICE_ID == '99' else LIMIT_EDIT_TO_CURRENT_COMMUNITY

# search behavior attribute see: base_searcher. Set to TRUE if you are deploying  a DB
# with multiple plots but you want default filter(?) to show current community instances.
# Central Server in BHP must always be set to FALSE.
FILTERED_DEFAULT_SEARCH = False if DEVICE_ID == '99' else FILTERED_DEFAULT_SEARCH
STUDY_OPEN_DATETIME = STUDY_OPEN_DATETIME

ADMIN_EXCLUDE_DEFAULT_CODE = ADMIN_EXCLUDE_DEFAULT_CODE
