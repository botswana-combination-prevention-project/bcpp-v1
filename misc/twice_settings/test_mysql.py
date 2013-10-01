from .common import *
from ._utils import mysql_base_config


db_pass = env_get('TEST_DB_PASSWORD')
mysql_config = customize(mysql_base_config, {'PASSWORD': db_pass})

DATABASES = {
    'default': customize(mysql_config, {'NAME': 'test_default'}),
    'dispatch_destination': customize(mysql_config, {'NAME': 'test_destination'}),
}
