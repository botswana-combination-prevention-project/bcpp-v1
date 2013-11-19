from .base import *
from ._utils import mysql_db


DEBUG = True

DEVICE_ID = '32'

TEMPLATE_DEBUG = DEBUG

KEY_PATH = join(SETTINGS_DIR, '..', '..', 'keys')

LOCALE_PATHS = ('locale', )

DATABASES = {
    'default': mysql_db(NAME='bhp066'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
    'bcpp038-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.174'),
    'bcpp035-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.216'),
}