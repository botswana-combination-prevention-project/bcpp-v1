import os
import sys
#import platform

SOURCE_ROOT = '~/source'

SOURCE_DIR = sys.path.expanduser(SOURCE_ROOT)
sys.path.insert(1, os.path.join(SOURCE_DIR, 'edc_project'))
sys.path.insert(1, os.path.join(SOURCE_DIR, 'lis_project'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
#if platform.system() == 'Darwin':
#        os.environ['PYTHON_EGG_CACHE'] = '/usr/local/pylons/python-eggs'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
