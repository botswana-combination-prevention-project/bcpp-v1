from os import environ

from django.core.exceptions import ImproperlyConfigured


mysql_base_config = {
    'ENGINE': 'django.db.backends.mysql',
    'OPTIONS': {
        'init_command': 'SET storage_engine=INNODB'
    },
    'USER': 'root',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '3306',
}

sqlite_base_config = {
    'ENGINE': 'django.db.backends.sqlite3',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': '',
    'PORT': ''
}


def env_get(var_name):
    """get an environment variable"""
    try:
        return environ[var_name]
    except:
        raise ImproperlyConfigured("Set the %s environment variable" % var_name)


def customize(base_dict, diff_dict):
    """Immutable dictionary updater or merger."""
    result = base_dict.copy()
    result.update(diff_dict)
    return result


#Things to put in your .bashrc or .bash_profile file
# export TEST_DB_PASSWORD=cc3721b
# export DEV_DB_PASSWORD='cc3721b'
# export PROD_DB_PASSWORD=cc3721b
# export SECRET_KEY=0$q&@p=jz(+_r^+phzenyqi49#y2^3ot3h#jru+32z&+cm&j51
# exportEMAIL_HOST_PASSWORD=paeH#ie9

# alias='export DJANGO_SETTINGS_MODULE=bhp066; python manage.py test'
