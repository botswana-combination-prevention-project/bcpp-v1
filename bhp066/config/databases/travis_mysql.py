
TRAVIS_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_default',
        'USER': 'travis',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_lab_api',
        'USER': 'travis',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'test_server': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_destination',
        'USER': 'travis',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
}
