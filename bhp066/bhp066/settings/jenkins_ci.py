from ._utils import sqlite_base_config, customize
from ._edc_apps import EDC_APPS
from ._lis_apps import LIS_APPS
from .common import *


SOUTH_TESTS_MIGRATE = False

db_pass = env('TEST_DB_PASSWORD')
sqlite_config = customize(sqlite_base_config, PASSWORD=db_pass)

DATABASES = {
    'default': customize(sqlite_config, NAME='lab'),
    'dispatch_destination': customize(sqlite_config, NAME='producer'),
}

INSTALLED_APPS += ('django_jenkins')

PROJECT_APPS = BCPP_APPS  # + BHP_LOCAL_APPS + LAB_LOCAL_APPS

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
)
