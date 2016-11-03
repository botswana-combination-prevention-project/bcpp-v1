import os
from unipath import Path

from .settings import *

BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
GIT_DIR = BASE_DIR.ancestor(1)
ETC_DIR = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1).child('export').child('etc')

# if remote, ssh -f -N -L 5000:127.0.0.1:3306 django@edc.bhp.org.bw
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(ETC_DIR, 'default.cnf'),
        },
        'ATOMIC_REQUESTS': True,
    },
}

FILTERED_DEFAULT_SEARCH = False
LIMIT_EDIT_TO_CURRENT_SURVEY = False
LIMIT_EDIT_TO_CURRENT_COMMUNITY = False
