from django.core.management.base import BaseCommand

from ...utils import update_replaceables


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = ''
    help = 'List the online and replaceable status of a producer'

    def handle(self, *args, **options):
        print('Updating replaceables ...')
        update_replaceables()
        print('Done.')
