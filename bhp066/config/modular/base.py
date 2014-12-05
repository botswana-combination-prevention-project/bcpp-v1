import platform
import sys
from os.path import realpath, abspath, join, dirname

from unipath import Path

from .logger import LOGGING

from ._utils import *


ADMINS = (('erikvw', 'ew@2789@gmail.com'),)

# Path
SETTINGS_DIR = dirname(realpath(__file__))  # needed??
SOURCE_DIR = Path(__file__).ancestor(4)
PROJECT_DIR = Path(__file__).ancestor(3)
MEDIA_ROOT = PROJECT_DIR.child('media')
STATIC_ROOT = PROJECT_DIR.child('static')
TEMPLATE_DIRS = (
    PROJECT_DIR.child('templates'),
)
STATICFILES_DIRS = ()
CONFIG_DIR = PROJECT_DIR.child('bhp066')
MAP_DIR = STATIC_ROOT.child('img')
DEFAULT_FILE_STORAGE = 'database_files.storage.DatabaseStorage'

MANAGERS = ADMINS

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
#langauage setting
ugettext = lambda s: s
LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
)

#LOCALE_PATHS = ('locale', )

LANGUAGE_CODE = 'tn'

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

#Map images storage table with blob field
DB_FILES = {
    'table': 'FILES',
    'base_url': 'http://localhost/dbfiles/'
}

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

ROOT_URLCONF = 'bhp066.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bhp066.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',   # DONT TOUCH!!
    'django_databrowse',
    'dajaxice',
    'storages',
    'dajax',
    #'south',

    'edc.apps.admin_supplemental_fields',
    'edc.apps.app_configuration',

    'edc.base.modeladmin',
    'edc.base.form',
    'edc.base.model',

    'edc.core.identifier',
    'edc.core.crypto_fields',
    'edc.core.model_data_inspector',
    'edc.core.model_selector',
    'edc.core.bhp_templates',
    'edc.core.bhp_static',
    'edc.core.bhp_string',
    'edc.core.bhp_userprofile',
    'edc.core.bhp_poll_mysql',
    'edc.core.bhp_templatetags',
    'edc.core.bhp_common',
    'edc.core.bhp_content_type_map',
    'edc.data_manager',
    'edc.core.bhp_variables',
    'edc.core.bhp_site_edc',
    'edc.core.bhp_nmap',
    'edc.core.bhp_context',
    'edc.core.bhp_using',
    'edc.core.bhp_export_data',
    'edc.core.bhp_birt_reports',

    'edc.device.inspector',
    'edc.device.dispatch',
    'edc.device.netbook',
    'edc.device.device',
    'edc.device.sync',

    'edc.dashboard.base',
    'edc.dashboard.search',
    'edc.dashboard.subject',
    'edc.dashboard.section',

    'edc.export',
    'edc.import',
    'edc.entry_meta_data',

    'edc.data_dictionary',

    'edc.map',

    'edc.testing',
    'edc.utils',

    'edc.subject.lab_tracker',
    'edc.subject.code_lists',
    'edc.subject.rule_groups',
    'edc.subject.actg',
    'edc.subject.entry',
    'edc.subject.consent',
    'edc.subject.contact',
    'edc.subject.locator',
    'edc.subject.subject_summary',
    'edc.subject.off_study',
    'edc.subject.registration',
    'edc.subject.appointment',
    'edc.subject.appointment_helper',
    'edc.subject.visit_schedule',
    'edc.subject.visit_tracking',
    'edc.subject.appointment',
    'edc.subject.subject',
    'edc.subject.subject_config',
    'edc.subject.adverse_event',

    'edc.lab.lab_clinic_api',
    'edc.lab.lab_clinic_reference',
    'edc.lab.lab_requisition',
    'edc.lab.lab_packing',
    'edc.lab.lab_profile',

    'lis.labeling',
    'lis.core.lab_common',
    'lis.core.lab_flag',
    'lis.core.lab_grading',
    'lis.core.lab_reference',
    'lis.core.lab_result_report',
    'lis.core.bhp_research_protocol',
    'lis.core.lock',

    'lis.specimen.lab_aliquot_list',
    'lis.specimen.lab_panel',
    'lis.specimen.lab_test_code',
    'lis.specimen.lab_receive',
    'lis.specimen.lab_aliquot',
    'lis.specimen.lab_order',
    'lis.specimen.lab_result',
    'lis.specimen.lab_result_item',

    'lis.subject.lab_account',
    'lis.subject.lab_patient',

    'lis.exim.lab_export',
    'lis.exim.lab_import',
    'lis.exim.lab_import_lis',
    'lis.exim.lab_import_dmis',

    'apps.bcpp',
    'apps.bcpp.app_configuration',
    'apps.bcpp_list',
    'apps.bcpp_dashboard',
    'apps.bcpp_stats',
    'apps.bcpp_household',
    'apps.bcpp_subject',
    'apps.bcpp_household_member',
    'apps.bcpp_lab',
    'apps.bcpp_survey',
    'apps.bcpp_inspector',
    'apps.bcpp_dispatch',
    'apps.bcpp_analytics',
#     'apps.bcpp_clinic_lab',
#     'apps.bcpp_clinic',
#     'apps.clinic',
#     'apps.bcpp_clinic_dashboard',
    'tastypie',
    'edc.audit',
)


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
APP_NAME = 'bcpp'
PROJECT_NUMBER = 'BHP066'
PROJECT_IDENTIFIER_PREFIX = '066'
PROJECT_IDENTIFIER_MODULUS = 7
PROJECT_TITLE = 'Botswana Combination Prevention Project'
PROTOCOL_REVISION = 'V1.0 24 September 2013'
INSTITUTION = 'Botswana-Harvard AIDS Institute Partnership'

# admin overrides
LOGIN_URL = '/{app_name}/login/'.format(app_name=APP_NAME)
LOGIN_REDIRECT_URL = '/{app_name}/'.format(app_name=APP_NAME)
LOGOUT_URL = '/{app_name}/logout/'.format(app_name=APP_NAME)

# south
SOUTH_LOGGING_FILE = join(dirname(__file__), "south.log")
SOUTH_LOGGING_ON = True

DEVICE_ID='99'
# dajax
DAJAXICE_MEDIA_PREFIX = "dajaxice"

# edc.subject.appointment
APPOINTMENTS_PER_DAY_MAX = 20
APPOINTMENTS_DAYS_FORWARD = 15

# edc.subject.registered_subject
SUBJECT_APP_LIST = ['bcpp_subject']
SUBJECT_TYPES = ['subject']
MAX_SUBJECTS = {'subject': 3000}

# edc.device.dispatch
DISPATCH_APP_LABELS = ['bcpp_subject', 'bcpp_household', 'bcpp_household_member', 'bcpp_lab']

# edc.crypto_fields
IS_SECURE_DEVICE = False
MAY_CREATE_NEW_KEYS = True
FIELD_MAX_LENGTH = 'migration'

# edc.map
CURRENT_COMMUNITY = 'molapowabojang'
CURRENT_COMMUNITY_CHECK = False       # turn this to true on the netbooks to make a community check is run on netbooks
CURRENT_MAPPER = CURRENT_COMMUNITY
GPS_FILE_NAME = '/Volumes/GARMIN/GPX/temp.gpx'
GPS_DEVICE = '/Volumes/GARMIN/'
GPX_TEMPLATE = join(STATIC_ROOT, 'gpx/template.gpx')
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

# edc.device.inspector (middleman)
MIDDLE_MAN_LIST = ['resourcemac-bhp066']

# edc.device.sync
ALLOW_MODEL_SERIALIZATION = True

#Stripped down EDC for purposes of CLO's work.
# DENIED_SECTIONS_FOR_GROUP = {'clo': ('household', 'subject', 'member', 'audit_trail', 'appointments', 'reports')}
# LOGGED_IN_USER_GROUP = 'clo'
