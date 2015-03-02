from ._utils import mysql_base_config, DBConfig, env
from .dev import *


mysql_db = DBConfig(mysql_base_config, PASSWORD=env('DEV_DB_PASSWORD'))

DATABASES = {
    'default': mysql_db(NAME='bhp066'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
    'mpp15-bhp066': mysql_db(NAME='bhp066_survey', HOST='192.168.1.36'),
}

INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ('127.0.0.1', )

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
