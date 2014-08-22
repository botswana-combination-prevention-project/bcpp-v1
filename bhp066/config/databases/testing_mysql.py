TESTING_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'test_default',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '',
        'PORT': '',
    },
    'dispatch_destination': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'test_destination',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '',
        'PORT': '',
    },
}
