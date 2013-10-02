from ._utils import mysql_base_config, DBConfig, env
from .dev import *

# Coulson's custom settings. To be modified only by him.
#To use this as your main settings file, on any shell session that you use type:
# $export DJANGO_SETTINGS_MODULE=bhp066.settings.dev_ckgathi

mysql_db = DBConfig(mysql_base_config, PASSWORD=env('DEV_DB_PASSWORD'))

DATABASES = {
    'default': mysql_db(NAME='bhp066_migrated'),
    'lab_api': mysql_db(NAME='lab', HOST='192.168.1.50'),
    'mpp15-bhp066': mysql_db(NAME='bhp066_survey', HOST='192.168.1.36'),
}


#Things to put in your .bashrc or .bash_profile file. If you don't the app will blow up
# export TEST_DB_PASSWORD=cc3721b
# export DEV_DB_PASSWORD='cc3721b'
# export PROD_DB_PASSWORD=cc3721b
# export SECRET_KEY=0$q&@p=jz(+_r^+phzenyqi49#y2^3ot3h#jru+32z&+cm&j51
# exportEMAIL_HOST_PASSWORD=paeH#ie9

# alias='export DJANGO_SETTINGS_MODULE=bhp066; python manage.py test'
