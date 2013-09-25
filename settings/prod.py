from .common import *
from ._utils import mysql_base_config, customize


db_pass = env_get('PROD_DB_PASSWORD')
mysql_config = customize(mysql_base_config, {'PASSWORD': db_pass})

DATABASES = {
    'default': customize(mysql_config, {'NAME': 'bhp066_migrated'}),
    'lab_api': customize(mysql_config, {'NAME': 'lab', 'HOST': '192.168.1.50'}),
    'mpp15-bhp066': customize(mysql_config, {'NAME': 'bhp066_survey', 'HOST': '192.168.1.36'})
}
