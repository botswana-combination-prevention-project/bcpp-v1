from ._utils import mysql_base_config, customize
from .dev import *

db_pass = env_get('DEV_DB_PASSWORD')
mysql_config = customize(mysql_base_config, {'PASSWORD': db_pass})

DATABASES = {
    'default': customize(mysql_config, {'NAME': 'bhp066'}),
    'lab_api': customize(mysql_config, {'NAME': 'lab', 'HOST': '192.168.1.50'}),
    'mpp15-bhp066': customize(mysql_config, {'NAME': 'bhp066_survey', 'HOST': '192.168.1.36'}),
}


INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ('127.0.0.1', )

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
