"""Common settings to all settings files"""
#import logger
import os
import platform

from unipath import Path

from ._utils import env
from ._edc_apps import EDC_APPS
from ._lis_apps import LIS_APPS

ADMINS = (('erikw', 'ew2789@gmail.com'),)
MANAGERS = ADMINS

#PROJECT_DIR = Path(__file__).ancestor(3)
FILE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.normpath(os.path.join(FILE_DIR, "../../../bhp066"))
#MEDIA_ROOT = PROJECT_DIR.child("media")
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")
STATIC_ROOT = os.path.join(PROJECT_DIR, "static")
#STATIC_ROOT = PROJECT_DIR.child("static")
#MAP_DIR = STATIC_ROOT.child('img')
MAP_DIR = os.path.join(STATIC_ROOT, 'img')
#LOCALE_PATHS = PROJECT_DIR.child("locale")
LOCALE_PATHS = os.path.join(PROJECT_DIR, "locale")
#CONFIG_DIR = PROJECT_DIR.child('bhp066')
CONFIG_DIR = os.path.join(PROJECT_DIR, 'bhp066')

ALLOWED_HOSTS = []

TIME_ZONE = 'Africa/Gaborone'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#langauage setting
ugettext = lambda s: s
LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
)

LANGUAGE_CODE = 'en'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (('django.template.loaders.cached.Loader',
                     ('django.template.loaders.filesystem.Loader',
                      'django.template.loaders.app_directories.Loader',
                      'django.template.loaders.eggs.Loader',)
                     ),
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

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages"
)

ROOT_URLCONF = 'bhp066.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bhp066.wsgi.application'

TEMPLATE_DIRS = (
    #PROJECT_DIR.child('templates'),
    os.path.join(PROJECT_DIR, 'templates'),
)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'django_databrowse',
)

THIRD_PARTY_APPS = (
    'south',
    'dajaxice',
    'dajax',
)

BCPP_APPS = (
    'apps.bcpp',
    'apps.bcpp_lab',
    'apps.bcpp_list',
    'apps.bcpp_subject',
    'apps.bcpp_dashboard',
    'apps.bcpp_stats',
    'apps.bcpp_household',
    'apps.bcpp_household_member',
    'apps.bcpp_survey',
    'apps.bcpp_inspector',
    'apps.bcpp_dispatch',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + BCPP_APPS + EDC_APPS + LIS_APPS

# email settings
EMAIL_HOST = '192.168.1.48'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'django'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

#SOUTH_LOGGING_FILE = Path(PROJECT_DIR, "south.log")
SOUTH_LOGGING_FILE = os.path.join(PROJECT_DIR, "south.log")
SOUTH_LOGGING_ON = True
AUTH_PROFILE_MODULE = "bhp_userprofile.userprofile"
# https://bitbucket.org/tyrion/django-autocomplete
AUTOCOMPLETE_MEDIA_PREFIX = '/media/autocomplete/media/'
DAJAXICE_MEDIA_PREFIX = "dajaxice"

# only for community server
IS_COMMUNITY_SERVER = True
ALLOW_DELETE_MODEL_FROM_SERIALIZATION = False
ALLOW_MODEL_SERIALIZATION = True

# EDC GENERAL SETTINGS
APP_NAME = 'bcpp'
PROJECT_NUMBER = 'BHP066'
PROJECT_IDENTIFIER_PREFIX = '066'
PROJECT_IDENTIFIER_MODULUS = 7
PROJECT_TITLE = 'Botswana Combination Prevention Project'
PROTOCOL_REVISION = 'V1.0 12 August 2013'
INSTITUTION = 'Botswana-Harvard AIDS Institute Partnership'
LOGIN_URL = '/{app_name}/login/'.format(app_name=APP_NAME)
LOGIN_REDIRECT_URL = '/{app_name}/'.format(app_name=APP_NAME)
LOGOUT_URL = '/{app_name}/logout/'.format(app_name=APP_NAME)
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'
LAB_LOCK_NAME = 'BHP066'
LABDB = 'bhplab'
SESSION_COOKIE_AGE = 3000
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SUBJECT_TYPES = ['subject']
MAX_SUBJECTS = {'subject': 3000}
APPOINTMENTS_PER_DAY_MAX = 20
APPOINTMENTS_DAYS_FORWARD = 15

SUBJECT_APP_LIST = ['bcpp_subject', 'bcpp_htc_subject']
DISPATCH_APP_LABELS = ['bcpp_subject', 'bcpp_htc_subject', 'bcpp_household', 'bcpp_household_member', 'bcpp_lab']

#Reports settings
REPORTS_TEMPLATES_PATH = PROJECT_DIR
#REPORTS_JAR_PATH = Path(PROJECT_DIR, 'birtreport_generator.jar')
REPORTS_JAR_PATH = os.path.join(PROJECT_DIR, 'birtreport_generator.jar')
#REPORTS_OUTPUT_PATH = PROJECT_DIR.child('bhp_birt_reports', 'templates')
REPORTS_OUTPUT_PATH = os.path.join(PROJECT_DIR, 'bhp_birt_reports/templates')

#BHP_CRYPTO_SETTINGS
IS_SECURE_DEVICE = False
MAY_CREATE_NEW_KEYS = True

GPS_FILE_PATH = '/Volumes/GARMIN/GPX/Current.gpx'
VERIFY_GPS = False
FIELD_MAX_LENGTH = 'migration'

# LAB REFERENCE AND GRADING
REFERENCE_RANGE_LIST = 'BHPLAB_NORMAL_RANGES_201005'
GRADING_LIST = 'DAIDS_2004'

# for bhp_import_dmis
if platform.system() == 'Darwin':
    LAB_IMPORT_DMIS_DATA_SOURCE = ('DRIVER=/usr/local/lib/libtdsodbc.so;SERVER=192.168.1.141;'
                                   'PORT=1433;UID=sa;PWD=cc3721b;DATABASE=BHPLAB')
else:
    LAB_IMPORT_DMIS_DATA_SOURCE = ('DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;'
                                   'DATABASE=BHPLAB')
VAR_ROOT = '/var'
#LOGGING = logger.LOGGING
CURRENT_MAPPER = 'mochudi'
CURRENT_SURVEY = 'baseline'

SUBJECT_IDENTIFIER_UNIQUE_ON_CONSENT = False  # set to False so that the constraint can be expanded to subject_identifier + survey"""Common settings to all settings files"""
#import logger
import platform

from unipath import Path

from ._utils import env
from ._edc_apps import EDC_APPS
from ._lis_apps import LIS_APPS

ADMINS = (('erikw', 'ew2789@gmail.com'),)
MANAGERS = ADMINS

PROJECT_DIR = Path(__file__).ancestor(3)
MEDIA_ROOT = PROJECT_DIR.child("media")
STATIC_ROOT = PROJECT_DIR.child("static")
MAP_DIR = STATIC_ROOT.child('img')
LOCALE_PATHS = PROJECT_DIR.child("locale")
CONFIG_DIR = PROJECT_DIR.child('bhp066')

ALLOWED_HOSTS = []

TIME_ZONE = 'Africa/Gaborone'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#langauage setting
ugettext = lambda s: s
LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
)

LANGUAGE_CODE = 'en'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (('django.template.loaders.cached.Loader',
                     ('django.template.loaders.filesystem.Loader',
                      'django.template.loaders.app_directories.Loader',
                      'django.template.loaders.eggs.Loader',)
                     ),
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

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages"
)

ROOT_URLCONF = 'bhp066.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bhp066.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'django_databrowse',
)

THIRD_PARTY_APPS = (
    'south',
    'dajaxice',
    'dajax',
)

BCPP_APPS = (
    'apps.bcpp',
    'apps.bcpp_lab',
    'apps.bcpp_list',
    'apps.bcpp_subject',
    'apps.bcpp_dashboard',
    'apps.bcpp_stats',
    'apps.bcpp_household',
    'apps.bcpp_household_member',
    'apps.bcpp_survey',
    'apps.bcpp_inspector',
    'apps.bcpp_dispatch',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + BCPP_APPS + EDC_APPS + LIS_APPS

SOUTH_LOGGING_FILE = Path(PROJECT_DIR, "south.log")
SOUTH_LOGGING_ON = True
AUTH_PROFILE_MODULE = "bhp_userprofile.userprofile"
# https://bitbucket.org/tyrion/django-autocomplete
AUTOCOMPLETE_MEDIA_PREFIX = '/media/autocomplete/media/'
DAJAXICE_MEDIA_PREFIX = "dajaxice"

# only for community server
IS_COMMUNITY_SERVER = True
ALLOW_DELETE_MODEL_FROM_SERIALIZATION = False
ALLOW_MODEL_SERIALIZATION = True

# EDC GENERAL SETTINGS
APP_NAME = 'bcpp'
PROJECT_NUMBER = 'BHP066'
PROJECT_IDENTIFIER_PREFIX = '066'
PROJECT_IDENTIFIER_MODULUS = 7
PROJECT_TITLE = 'Botswana Combination Prevention Project'
PROTOCOL_REVISION = 'V1.0 12 August 2013'
INSTITUTION = 'Botswana-Harvard AIDS Institute Partnership'
LOGIN_URL = '/{app_name}/login/'.format(app_name=APP_NAME)
LOGIN_REDIRECT_URL = '/{app_name}/'.format(app_name=APP_NAME)
LOGOUT_URL = '/{app_name}/logout/'.format(app_name=APP_NAME)
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i'
LAB_LOCK_NAME = 'BHP066'
LABDB = 'bhplab'
SESSION_COOKIE_AGE = 3000
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SUBJECT_TYPES = ['subject']
MAX_SUBJECTS = {'subject': 3000}
APPOINTMENTS_PER_DAY_MAX = 20
APPOINTMENTS_DAYS_FORWARD = 15

SUBJECT_APP_LIST = ['bcpp_subject', 'bcpp_htc_subject']
DISPATCH_APP_LABELS = ['bcpp_subject', 'bcpp_htc_subject', 'bcpp_household', 'bcpp_household_member', 'bcpp_lab']

#Reports settings
REPORTS_TEMPLATES_PATH = PROJECT_DIR
REPORTS_JAR_PATH = Path(PROJECT_DIR, 'birtreport_generator.jar')
REPORTS_OUTPUT_PATH = PROJECT_DIR.child('bhp_birt_reports', 'templates')

#BHP_CRYPTO_SETTINGS
IS_SECURE_DEVICE = False
MAY_CREATE_NEW_KEYS = True

GPS_FILE_PATH = '/Volumes/GARMIN/GPX/Current.gpx'
VERIFY_GPS = False
FIELD_MAX_LENGTH = 'migration'

# LAB REFERENCE AND GRADING
REFERENCE_RANGE_LIST = 'BHPLAB_NORMAL_RANGES_201005'
GRADING_LIST = 'DAIDS_2004'

# for bhp_import_dmis
if platform.system() == 'Darwin':
    LAB_IMPORT_DMIS_DATA_SOURCE = ('DRIVER=/usr/local/lib/libtdsodbc.so;SERVER=192.168.1.141;'
                                   'PORT=1433;UID=sa;PWD=cc3721b;DATABASE=BHPLAB')
else:
    LAB_IMPORT_DMIS_DATA_SOURCE = ('DRIVER={FreeTDS};SERVER=192.168.1.141;UID=sa;PWD=cc3721b;'
                                   'DATABASE=BHPLAB')
VAR_ROOT = '/var'
#LOGGING = logger.LOGGING
CURRENT_MAPPER = 'mochudi'
CURRENT_SURVEY = 'baseline'

SUBJECT_IDENTIFIER_UNIQUE_ON_CONSENT = False  # set to False so that the constraint can be expanded to subject_identifier + survey
