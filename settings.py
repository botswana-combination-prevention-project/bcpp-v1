# Django settings for bhp project.
import os
import platform
import logger

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DIRNAME = os.path.dirname(__file__)
ADMINS = (
    ('erikvw', 'ew@2789@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '',
        'PORT': '',
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'lab',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.1.50',
        'PORT': '3306',
    },
}

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
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(DIRNAME, '')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(DIRNAME, 'static')

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

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.request",
                               "django.contrib.messages.context_processors.messages")

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, 'bhp_templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'databrowse',
    'django_extensions',
    'dajaxice',
    'dajax',
    'south',
    'audit_trail',
    'autocomplete',
    'bhp_templates',
    'bhp_static',
    'bhp_crypto',
    'bhp_string',
    'bhp_lock',
    'bhp_appointment_helper',
    'bhp_userprofile',
    'bhp_poll_mysql',
    'bhp_model_selector',
    'bhp_templatetags',
    'bhp_calendar',
    'bhp_base_model',
    'bhp_actg_reference',
    'bhp_adverse',
#     'bhp_haart',
    'bhp_code_lists',
    'bhp_common',
    'bhp_identifier',
    'bhp_content_type_map',
    'bhp_search',
    'bhp_section',
    'bhp_consent',
    'bhp_locator',
    'bhp_off_study',
    'bhp_registration',
    'bhp_botswana',
    'bhp_data_manager',
    'bhp_base_admin',
    'bhp_base_form',
    'bhp_variables',
    'bhp_research_protocol',
    'bhp_sync',
    'bhp_device',
    'lab_common',
    'lab_import',
    'lab_import_lis',
    'lab_import_dmis',
    'lab_flag',
    'lab_grading',
    'lab_reference',
    'lab_requisition',
    'lab_aliquot_list',
    'lab_base_model',
    'lab_panel',
    'lab_test_code',
    'lab_account',
    'lab_patient',
    'lab_receive',
    'lab_aliquot',
    'lab_order',
    'lab_result',
    'lab_result_item',
    'lab_barcode',
    'lab_clinic_api',
    'lab_clinic_reference',
    'lab_export',
    'lab_result_report',
    'lab_packing',
    'lab_base_model',
    'bhp_lab_tracker',
    'bhp_visit',
    'bhp_visit_tracking',
    'bhp_appointment',
    'bhp_subject',
    'bhp_nmap',
    'bhp_data_manager',
#     'bhp_eligibility',
    'bhp_entry',
    'bhp_lab_entry',
#     'bhp_list',
    'bhp_context',
#     'bhp_statistics',
    'bhp_using',
    'bhp_contact',
    'bhp_dashboard',
    'bhp_dashboard_registered_subject',
    'bhp_export_data',
    'bhp_model_describer',
    'bhp_subject_summary',
    'bhp_entry_rules',
    'bhp_dispatch',
    'bhp_netbook',
#     'ph_dispenser',
    'bcpp',
    'bcpp_lab',
    'bcpp_list',
    'bcpp_subject',
    'bcpp_dashboard',
    'bcpp_stats',
    'bcpp_household',
    'bcpp_survey',
#     'bcpp_survey_dashboard',
#     'bcpp_survey_lab',
)

# email settings
EMAIL_HOST = '192.168.1.48'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'django'
EMAIL_HOST_PASSWORD = 'paeH#ie9'
EMAIL_USE_TLS = True

SOUTH_LOGGING_FILE = os.path.join(os.path.dirname(__file__), "south.log")
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
PROTOCOL_REVISION = 'V1.0 12 April 2013'
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
DEVICE_ID = '99'
MAX_SUBJECTS = 3000
APPOINTMENTS_PER_DAY_MAX = 20
APPOINTMENTS_DAYS_FORWARD = 15

SUBJECT_APP_LIST = ['bcpp_subject']

#BHP_CRYPTO_SETTINGS
IS_SECURE_DEVICE = False
MAY_CREATE_NEW_KEYS = True
#KEY_PATH = os.path.join(DIRNAME, 'keys')
KEY_PATH = '/Volumes/bhp066/keys'
#FIELD_MAX_LENGTH='default'
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
LOGGING = logger.LOGGING
