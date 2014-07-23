from .base import *
from ._utils import mysql_db


SOUTH_TESTS_MIGRATE = False

DATABASES = {
    'default': mysql_db(NAME='test_default'),
    'dispatch_destination': mysql_db(NAME='test_destination'),
}
