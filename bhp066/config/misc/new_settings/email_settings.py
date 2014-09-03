from ._utils import env
# email settings
EMAIL_HOST = '192.168.1.48'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'edcdev'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True