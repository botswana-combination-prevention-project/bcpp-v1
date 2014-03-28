from .base import *
from ._utils import mysql_db


DEBUG = True

DEVICE_ID = '92'

TEMPLATE_DEBUG = DEBUG

KEY_PATH = join(SETTINGS_DIR, '..', '..', 'keys')

LOCALE_PATHS = ('locale', )

testing_db_name = 'sqlite'
if 'test' in sys.argv:
    # make tests faster
    SOUTH_TESTS_MIGRATE = False
    if testing_db_name == 'sqlite':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'default',
                'USER': 'root',
                'PASSWORD': 'cc3721b',
                'HOST': '',
                'PORT': ''},
            'lab_api': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'lab',
                'USER': 'root',
                'PASSWORD': 'cc3721b',
                'HOST': '',
                'PORT': '',
            },
#             'survey': {
#                 'ENGINE': 'django.db.backends.sqlite3',
#                 'NAME': 'survey',
#                 'USER': 'root',
#                 'PASSWORD': 'cc3721b',
#                 'HOST': '',
#                 'PORT': '',
#             },
            'dispatch_destination': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'producer',
                'USER': 'root',
                'PASSWORD': 'cc3721b',
                'HOST': '',
                'PORT': '',
            },
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB',
                },
                'NAME': 'test_default',
                'USER': 'root',
                'PASSWORD': 'cc3721b',
                'HOST': '',
                'PORT': '',
            },
            'dispatch_destination': {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB',
                },
                'NAME': 'test_destination',
                'USER': 'root',
                'PASSWORD': 'cc3721b',
                'HOST': '',
                'PORT': '',
            },
        }
else:
    DATABASES = {
        'default': mysql_db(NAME='bhp066_re'),
        'lab_api': mysql_db(NAME='lab', HOST=''),
#         'bcpp024-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.191'),
#         'bcpp027-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.135'),
#         'bcpp021-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.159'),
#         'bcpp029-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.121'),
#         'bcpp034-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.143'),
#         'bcpp033-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.125'),
#         'bcpp023-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.229'),
#         'bcpp019-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.60'),
#         'bcpp025-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.139'),
#         'bcpp032-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.110'),
#         'bcpp037-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.186'),
#         'bcpp024-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.191'),
#         'bcpp007-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.108'),
#         'bcpp011-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.154'),
#         'bcpp006-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.218'),
#         'bcpp018-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.34'),
#         'bcpp002-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.136'),
#         'bcpp017-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.39'),
#         'bcpp008-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.155'),
#         'bcpp028-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.88'),
#         'bcpp001-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.198'),
#         'bcpp004-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.33'),
#         'bcpp012-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.26'),
#         'bcpp009-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.250'),
#         'bcpp014-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.37'),
#         'bcpp003-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.170'),
#         'bcpp016-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.47'),
#         'bcpp010-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.71'),
#         'bcpp026-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.109'),
#         'bcpp020-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.138'),
#         'bcpp030-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.54'),
        }

INSTALLED_APPS += ('debug_toolbar',)

INTERNAL_IPS = ('127.0.0.1', )

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
