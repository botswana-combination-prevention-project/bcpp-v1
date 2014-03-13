to create a db without using migrations
edit settings.py and comment out south in INSTALLED_APPS
run::
python manage.py syncdb
edit settings.py and uncomment south in INSTALLED_APPS
python manage.py syncdb
python manage.py migrate --fake
