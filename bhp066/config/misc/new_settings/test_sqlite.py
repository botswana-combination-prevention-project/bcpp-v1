from .common import *
from ._utils import sqlite_base_config, env, DBConfig


SOUTH_TESTS_MIGRATE = False

sqlite_db = DBConfig(sqlite_base_config, PASSWORD=env('TEST_DB_PASSWORD'))

DATABASES = {
    'default': sqlite_db(NAME='lab'),
    'dispatch_destination': sqlite_db(NAME='producer'),
}
