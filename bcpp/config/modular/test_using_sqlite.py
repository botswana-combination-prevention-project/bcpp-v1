from .base import *
from ._utils import sqlite_db

SOUTH_TESTS_MIGRATE = False

DATABASES = {
    'default': sqlite_db(NAME='default'),
    'lab_api': sqlite_db(NAME='lab'),
    'dispatch_destination': sqlite_db(NAME='producer'),
}
