from django.core.management.base import BaseCommand, CommandError
from bhp_crypto.utils import setup_new_keys


class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Generate new encryption keys.'

    def handle(self, *args, **options):

        #try:
        setup_new_keys()
        #except:
        #    CommandError('Failed to generate new encryption keys.')
