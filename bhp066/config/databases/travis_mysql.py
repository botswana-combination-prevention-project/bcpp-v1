
TRAVIS_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bcpp',
        'USER': 'travis',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bcpp_lab',
        'USER': 'travis',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
    'test_server': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bcpp_test',
        'USER': 'travis',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    },
}
