import pprint

from django.core.management.base import BaseCommand
from django.conf import settings

from bhp066.config.inspect_settings import settings_list


class Command(BaseCommand):

    args = ''
    help = 'Inspect settings attr: value'

    def handle(self, *args, **options):
        pp = pprint.PrettyPrinter(indent=4)
        settings_list.sort()
        for item in settings_list:
            x = {item: getattr(settings, item)}
            pp.pprint(x)
