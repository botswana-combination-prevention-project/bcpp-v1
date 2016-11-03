from .common import *
from ._utils import mysql_base_config, DBConfig, env


mysql_db = DBConfig(mysql_base_config, PASSWORD=env('DPROD_DB_PASSWORD'))

DATABASES = {
    'default': mysql_db(NAME='bhp066_migrated'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
    'mpp15-bhp066': mysql_db(NAME='bhp066_survey', HOST='192.168.1.36'),
}
