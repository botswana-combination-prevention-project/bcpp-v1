from .common import *
from ._utils import mysql_base_config, DBConfig, env


mysql_db = DBConfig(mysql_base_config, PASSWORD=env('DEV_DB_PASSWORD'))

DATABASES = {
    'default': mysql_db(NAME='test_default'),
    'dispatch_destination': mysql_db(NAME='test_destination'),
}
