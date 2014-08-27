import os
from unipath import Path

PATH = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1).child('etc')

PRODUCTION_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(PATH, 'default.cnf'),
        },
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(PATH, 'lab_api.cnf'),
        },
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'bcpp010-bhp066': {
         'ENGINE': 'django.db.backends.mysql',
         'OPTIONS': {
             'init_command': 'SET storage_engine=INNODB',
         },
         'NAME': 'bhp066',
         'USER': 'root',
         'PASSWORD': 'cc3721b',
         'HOST': '192.168.1.146',
         'PORT': '',
     },
}
