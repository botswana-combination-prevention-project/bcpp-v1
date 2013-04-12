LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        #'debug_console': {
        #    'level': 'DEBUG',
        #    'class': 'logging.StreamHandler',
        #    'formatter': 'simple',
        #},
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            #'filters': ['special']
        }
    },
   'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
       'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'bhp_crypto.classes.cryptor': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
        'lab_clinic_api.managers.lab_manager': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
        'lab_clinic_api.classes.updater': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
        'lab_clinic_api.management.commands.update_labs': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
        'lab_import_dmis.classes.dmis': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
        'lab_import.classes.base_lock': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
        'lab_import_lis.classes.lis': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
        'lab_import.classes.base_import_history': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
       'lab_clinic_api.managers.lab_manager': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
       'lab_clinic_api.managers.result_manager': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
       'lab_flag.classes.flag': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
       'lab_clinic_api.classes.dmis_result': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
       'lab_clinic_reference.classes.import_reference_range': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
       'lab_clinic_reference.classes.base_import': {
            'handlers': ['console', ],
            'level': 'INFO',
            #'filters': ['special']
        },
       'lab_receive.classes.receive_identifier': {
            'handlers': ['console', ],
            'level': 'WARNING',
            #'filters': ['special']
        },
    }
}