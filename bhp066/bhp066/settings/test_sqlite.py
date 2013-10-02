from .common import *
from ._utils import sqlite_base_config, env, DBConfig


SOUTH_TESTS_MIGRATE = False

#db_pass = env_get('TEST_DB_PASSWORD')
#sqlite_config = customize(sqlite_base_config, PASSWORD=db_pass)

sqlite_db = DBConfig(sqlite_base_config, PASSWORD=env('TEST_DB_PASSWORD'))

#DATABASES = {
    #'default': customize(sqlite_config, NAME='lab'),
    #'dispatch_destination': customize(sqlite_config, NAME='producer'),
#}

DATABASES = {
    'default': sqlite_db(NAME='lab'),
    'dispatch_destination': sqlite_db(NAME='producer'),
}
