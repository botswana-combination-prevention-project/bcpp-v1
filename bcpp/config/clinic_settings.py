import os
import platform
import sys

from unipath import Path
from installed_apps import DJANGO_APPS, THIRD_PARTY_APPS, EDC_APPS, LIS_APPS, LOCAL_APPS

from .databases import TESTING_SQLITE
from .databases import TESTING_MYSQL
from .databases import PRODUCTION_MYSQL

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (('erikvw', 'ew@2789@gmail.com'),)

# Path
DIRNAME = os.path.dirname(os.path.abspath(__file__))  # needed??
SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(3)  # e.g. /home/django/source

SOURCE_DIR = Path(__file__).ancestor(3)
PROJECT_DIR = Path(__file__).ancestor(2)
ETC_DIR = PROJECT_DIR.child('config').child('etc')  # for production this should be /etc/edc
EDC_DIR = SOURCE_ROOT.child('edc_project').child('edc')  # e.g. /home/django/source/edc_project/edc
TEMPLATE_DIRS = (
    EDC_DIR.child('templates'),
)
FIXTURE_DIRS = (
    PROJECT_DIR.child('apps', 'bcpp', 'fixtures'),
    )

MEDIA_ROOT = PROJECT_DIR.child('media')
STATIC_ROOT = PROJECT_DIR.child('static')
PROJECT_ROOT = Path(__file__).ancestor(3)  # e.g. /home/django/source/bhp066_project

STATICFILES_DIRS = ()
CONFIG_DIR = PROJECT_DIR.child('bhp066_clinic')
MAP_DIR = STATIC_ROOT.child('img')

# edc.crytpo_fields encryption keys   # DONT DELETE ME!!, just comment out
KEY_PATH = '/Users/melissa/Documents/git/source/bhp066_clinic/bhp066/keys'
# KEY_PATH = '/Users/ckgathi/source/confirm_plots/bhp066/keys'
# KEY_PATH = '/Users/sirone/Documents/workspace/git_projects/bhp066_git/bhp066/keys'
# KEY_PATH = '/Volumes/keys'

MANAGERS = ADMINS

# DATABASES
CONN_MAX_AGE = 15
testing_db_name = 'sqlite'
if 'test' in sys.argv:
    # make tests faster
    SOUTH_TESTS_MIGRATE = False
    if testing_db_name == 'sqlite':
        DATABASES = TESTING_SQLITE
    else:
        DATABASES = TESTING_MYSQL
else:
    DATABASES = PRODUCTION_MYSQL

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

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

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# URL prefix for admin media -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

# A list of locations of additional static files
STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0$q&@p=jz(+_r^+phzenyqi49#y2^3ot3h#jru+32z&+cm&j51'

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
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.request",
                               "django.contrib.messages.context_processors.messages")

ROOT_URLCONF = 'config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'config.wsgi.application'

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + EDC_APPS + LIS_APPS + LOCAL_APPS

# django
SESSION_COOKIE_AGE = 10000
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# django email settings
EMAIL_HOST = '192.168.1.48'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'edcdev'
EMAIL_HOST_PASSWORD = 'cc3721b'
EMAIL_USE_TLS = True
EMAIL_AFTER_CONSUME = False

# django auth
AUTH_PROFILE_MODULE = "bhp_userprofile.userprofile"

# general
APP_NAME = 'bcpp_clinic'
PROJECT_NUMBER = 'BHP066'
PROJECT_IDENTIFIER_PREFIX = '066'
PROJECT_IDENTIFIER_MODULUS = 7
PROJECT_TITLE = 'BCPP Clinic'
PROTOCOL_REVISION = 'V1.0 December 2013'
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

# edc.subject.appointment
APPOINTMENTS_PER_DAY_MAX = 20
APPOINTMENTS_DAYS_FORWARD = 15

# edc.subject.registered_subject
SUBJECT_APP_LIST = ['bcpp_clinic']
SUBJECT_TYPES = ['subject']
MAX_SUBJECTS = {'subject': 3000}

DISPATCH_APP_LABELS = ['bcpp_clinic', 'bcpp_clinic_lab', 'bcpp_clinic_dashboard']

# edc.crypto_fields
IS_SECURE_DEVICE = False
MAY_CREATE_NEW_KEYS = True
FIELD_MAX_LENGTH = 'migration'

# edc.map
SITE_CODE = '16'
CURRENT_COMMUNITY = 'Lentsweletau'
CURRENT_COMMUNITY_CHECK = False  # turn this to true on the netbooks to make a community check is run on netbooks
CURRENT_MAPPER = CURRENT_COMMUNITY
GPS_FILE_NAME = '/Volumes/GARMIN/GPX/temp.gpx'
GPS_DEVICE = '/Volumes/GARMIN/'
#GPX_TEMPLATE = os.path.join(STATIC_ROOT, 'gpx/template.gpx')
VERIFY_GPS = False

# edc.lab
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

# edc.device.device
DEVICE_ID = '99'
SERVER_DEVICE_ID_LIST = [91, 92, 93, 94, 95, 96, 97, 99]
MIDDLEMAN_DEVICE_ID_LIST = [98]
# edc.device.sync
ALLOW_MODEL_SERIALIZATION = True
