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
    'bcpp001-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.8',
        'PORT': '3306',
    },
    'bcpp008-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.24',
        'PORT': '3306',
    },
    'bcpp015-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.16',
        'PORT': '3306',
    },
    'bcpp022-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.2',
        'PORT': '3306',
    },
    'bcpp023-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.3',
        'PORT': '3306',
    },
    'bcpp024-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.11',
        'PORT': '3306',
    },
    'bcpp027-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.7',
        'PORT': '3306',
    },
    'bcpp028-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.6',
        'PORT': '3306',
    },
    'bcpp031-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.15',
        'PORT': '3306',
    },
    'bcpp035-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.9',
        'PORT': '3306',
    },
    'bcpp037-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.10',
        'PORT': '3306',
    },
    'bcpp039-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.12',
        'PORT': '3306',
    },
    'bcpp040-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.13',
        'PORT': '3306',
    },
    'bcpp051-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.17',
        'PORT': '3306',
    },
    'bcpp053-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.18',
        'PORT': '3306',
    },
    'bcpp054-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.19',
        'PORT': '3306',
    },
    'bcpp056-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.20',
        'PORT': '3306',
    },
    'bcpp063-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.29',
        'PORT': '3306',
    },
    'bcpp062-bhp066': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        },
        'NAME': 'bhp066',
        'USER': 'root',
        'PASSWORD': 'cc3721b',
        'HOST': '192.168.46.28',
        'PORT': '3306',
    }
}
