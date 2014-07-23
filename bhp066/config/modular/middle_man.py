from .base import *


DATABASES = {
    'default': mysql_db(NAME='bhp066'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
}

KEY_PATH = join(SETTINGS_DIR, '..', '..', 'keys')

LOCALE_PATHS = ('locale', )

# edc.device.device
DEVICE_ID = '98'

# edc.device.inspector (middleman)
MIDDLE_MAN_LIST = ['resourcemac-bhp066']

# edc.device.sync
ALLOW_MODEL_SERIALIZATION = True
