import os
import sys
import platform
#import djcelery
#djcelery.setup_loader()

if platform.system() == 'Darwin':
        home_dir = 'Users'
else:
        home_dir = 'home'

path = '/{0}/django/source'.format(home_dir)
if path not in sys.path:
    sys.path.append(path)
<<<<<<< .mine

path = '/{0}/django/source/bhp066'.format(home_dir)
=======
 
path = '/home/django/source/bhp062'
>>>>>>> .r160
if path not in sys.path:
    sys.path.append(path)
<<<<<<< .mine

path = '/{0}/django/source/bhp066/keys'.format(home_dir)
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bhp066.settings'

if platform.system() == 'Darwin':
        os.environ['PYTHON_EGG_CACHE'] = '/usr/local/pylons/python-eggs'

=======
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'bhp062.settings'
 
>>>>>>> .r160
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
