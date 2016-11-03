from django.core.management.base import BaseCommand
from django.db.models import Max

from edc.device.sync.models import Producer

from bhp066.apps.bcpp_household.models import Replaceable
from bhp066.apps.bcpp_household.utils import get_producer_status


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = ''
    help = 'List the online and replaceable status of a producer'

    def handle(self, *args, **options):
        producers = []
        print('replaceables_count: {}'.format(Replaceable.objects.filter(
            replaced=False).count()))
        print('replaceables_last_updated: {}'.format(Replaceable.objects.filter(
            replaced=False).aggregate(Max('created')).get('created_max')))
        for producer in Producer.objects.filter(is_active=True):
            producer_status = get_producer_status(producer)
            producers.append(producer_status)
        for producer_status in producers:
            print producer_status.producer_name
            print('  settings_key: ' + str(producer_status.settings_key))
            print('  IP: ' + str(producer_status.ip))
            print('  online: ' + str(producer_status.online))
            print('  sync\'ed: ' + str(producer_status.synced))
            print('  replaceables: ' + str(producer_status.replaceables_count))
            print('  replaceable last updated: ' + str(producer_status.replaceables_last_updated))
            if producer_status.error:
                print('  ' + str(producer_status.error_message))
            print ('---')
