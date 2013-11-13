from .base import *
from ._utils import mysql_db


DEBUG = True

DEVICE_ID = '99'

TEMPLATE_DEBUG = DEBUG

KEY_PATH = join(SETTINGS_DIR, '..', '..', 'keys')

LOCALE_PATHS = ('locale', )

DATABASES = {
    'default': mysql_db(NAME='bhp066'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
    'bcpp022-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.51'),
}
