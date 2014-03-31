from .base import *
from ._utils import mysql_db


DEBUG = True

TEMPLATE_DEBUG = DEBUG

KEY_PATH = join(SETTINGS_DIR, '..', '..', 'keys')

LOCALE_PATHS = ('locale',)

DATABASES = {
    'default': mysql_db(NAME='bcpp'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
}

INSTALLED_APPS += ('debug_toolbar', 'aldjemy')

INTERNAL_IPS = ('127.0.0.1', )

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
