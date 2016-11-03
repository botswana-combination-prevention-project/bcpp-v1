import socket

from .base import *

DEVICE_ID = '88'

KEY_PATH = '/Volumes/keys'

STATIC_ROOT = '/Users/django/Sites/bcppstudy/static/'

MAP_DIR = '/Users/django/Sites/bcppstudy/static/img/'

LOCALE_PATHS = ('/Users/django/source/bhp066_project/bhp066/locale', )

DATABASES = {
    'default': mysql_db(NAME='bhp066'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
}
