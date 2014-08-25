import os

# this could be /etc/mysql/django/ for security
PATH = os.path.expanduser('~/source/bhp066_project/bhp066/config/etc/')

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
}
