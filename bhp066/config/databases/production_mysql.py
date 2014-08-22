PRODUCTION_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '',
        'PORT': '',
    },
    'lab_api': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'lab',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '',
        'PORT': '',
    },
}
