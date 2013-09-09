import simplejson as json
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model
#from bhp_sync.models import Producer


class Command(BaseCommand):

    args = ()
    help = 'Update settings file DATABASE attribute with current producer list. '

    def handle(self, *args, **options):

        filename = 'settings_netbook.py'
        databases = {}
        Producer = get_model('bhp_sync', 'producer')
        for producer in Producer.objects.filter(settings_key__isnull=False):
            databases.update({producer.settings_key: {
                'ENGINE': 'django.db.backends.mysql',
                'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB',
                },
                'NAME': 'bhp041_survey',
                'USER': 'root',
                'PASSWORD': 'cc3721b',
                'HOST': '{ip}'.format(ip=producer.url.replace('/', '').replace('http:', '')),
                'PORT': '3306',
            }})
        f = open(filename, 'w')
        f.seek(0)
        f.write('DATABASES={{{0}}}'.format(json.dumps(databases, sort_keys=True, indent=4)))
        f.truncate()
        f.close()
