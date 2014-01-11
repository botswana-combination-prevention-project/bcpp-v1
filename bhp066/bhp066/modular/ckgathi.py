from .base import *
from ._utils import mysql_db


DEBUG = True

DEVICE_ID = '92'

TEMPLATE_DEBUG = DEBUG

KEY_PATH = join(SETTINGS_DIR, '..', '..', 'keys')

LOCALE_PATHS = ('locale', )

DATABASES = {
    'default': mysql_db(NAME='bhp066_clo'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
    'bcpp024-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.191'),
    'bcpp027-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.135'),
    'bcpp021-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.159'),
    'bcpp029-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.121'),
    'bcpp034-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.181'),
    'bcpp033-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.125'),
    'bcpp023-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.229'),
    'bcpp019-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.60'),
    'bcpp025-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.139'),
    'bcpp032-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.110'),
    'bcpp037-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.186'),
    'bcpp024-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.191'),
#     'bcpp035-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.216'),
}
