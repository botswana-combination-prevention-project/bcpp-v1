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
    'bcpp034-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.143'),
    'bcpp033-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.125'),
    'bcpp023-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.229'),
    'bcpp019-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.60'),
    'bcpp025-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.139'),
    'bcpp032-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.110'),
    'bcpp037-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.186'),
    'bcpp024-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.191'),
    'bcpp007-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.108'),
    'bcpp011-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.154'),
    'bcpp006-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.218'),
    'bcpp018-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.34'),
    'bcpp002-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.136'),
    'bcpp017-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.39'),
    'bcpp008-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.155'),
    'bcpp028-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.88'),
    'bcpp001-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.198'),
    'bcpp004-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.33'),
    'bcpp012-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.26'),
    'bcpp009-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.250'),
    'bcpp014-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.37'),
    'bcpp003-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.170'),
    'bcpp016-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.47'),
    'bcpp010-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.71'),
    'bcpp026-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.109'),
    'bcpp020-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.138'),
    'bcpp030-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.54'),
#     'bcpp035-bhp066': mysql_db(NAME='bhp066', HOST='192.168.1.216'),
}
