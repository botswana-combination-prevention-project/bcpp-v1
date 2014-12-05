from django.conf import settings

# from config.settings import ADMINS
# from config.mail_settings import (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
#                             EMAIL_HOST_PASSWORD, EMAIL_USE_TLS)

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'amqp://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Africa/Gaborone'
CELERY_ENABLE_UTC = True


def my_on_failure(self, exc, task_id, args, kwargs, einfo):
    pass

CELERY_ANNOTATIONS = {'*': {'on_failure': my_on_failure}}

CELERY_SEND_TASK_ERROR_EMAILS = True
ADMINS = settings.ADMINS
SERVER_EMAIL = 'celery@bhp.org.bw'
EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = settings.EMAIL_USE_TLS
