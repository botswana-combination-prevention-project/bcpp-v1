from ._utils import mysql_base_config
from .dev import *

# Sir One 's custom settings. To be modified only by him.
#To use this as your main settings file, on any shell session that you use type:
# $export DJANGO_SETTINGS_MODULE=appname.settings.dev_sirone

db_pass = env('DEV_DB_PASSWORD')
mysql_config = customize(mysql_base_config, PASSWORD=db_pass)

DATABASES = {
    'default': customize(mysql_config, NAME='bhp066_migrated'),
    'lab_api': customize(mysql_config, NAME='lab', HOST='192.168.1.50'),
    'mpp15-bhp066': customize(mysql_config, NAME='bhp066_survey', HOST='192.168.1.36'),
}



#Things to put in your .bashrc or .bash_profile file. If you don't the app will blow up
# export TEST_DB_PASSWORD=cc3721b
# export DEV_DB_PASSWORD='cc3721b'
# export PROD_DB_PASSWORD=cc3721b
# export SECRET_KEY=0$q&@p=jz(+_r^+phzenyqi49#y2^3ot3h#jru+32z&+cm&j51
# exportEMAIL_HOST_PASSWORD=paeH#ie9

# alias='export DJANGO_SETTINGS_MODULE=bhp066; python manage.py test'
