from ._utils import sqlite_base_config, DBConfig, env
from ._edc_apps import EDC_APPS
from ._lis_apps import LIS_APPS
from .common import *


SOUTH_TESTS_MIGRATE = False

sqlite_db = DBConfig(sqlite_base_config, PASSWORD=env('DEV_DB_PASSWORD'))

DATABASES = {
    'default': sqlite_db(NAME='lab'),
    'dispatch_destination': sqlite_db(NAME='producer'),
}

INSTALLED_APPS += ('django_jenkins')

PROJECT_APPS = BCPP_APPS  # + BHP_LOCAL_APPS + LAB_LOCAL_APPS

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
)
