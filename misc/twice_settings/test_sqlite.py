from .common import *
from _utils import sqlite_base_config


SOUTH_TESTS_MIGRATE = False

db_pass = env_get('TEST_DB_PASSWORD')
sqlite_config = customize(sqlite_base_config, {'PASSWORD': db_pass})

DATABASES = {
    'default': customize(sqlite_config, {'NAME': 'lab'}),
    'dispatch_destination': customize(sqlite_config, 'producer'),
}
