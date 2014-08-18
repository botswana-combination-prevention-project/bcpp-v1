import os
import sys
import site
#import platform



SOURCE_ROOT = '~/source'
VIRTUALENV_PATH = os.path.expanduser('~/.virtualenvs/django-1.6.5/')

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(os.path.join(VIRTUALENV_PATH, 'local/lib/python2.7/site-packages'))

SOURCE_DIR = sys.path.expanduser(SOURCE_ROOT)
sys.path.insert(1, os.path.join(SOURCE_DIR, 'edc_project'))
sys.path.insert(1, os.path.join(SOURCE_DIR, 'lis_project'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

#if platform.system() == 'Darwin':
#        os.environ['PYTHON_EGG_CACHE'] = '/usr/local/pylons/python-eggs'

# Activate your virtual env
activate_env=os.path.join(os.path.join(VIRTUALENV_PATH, 'bin/activate_this.py"))
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
