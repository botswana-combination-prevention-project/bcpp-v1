import logging
from django.core.management.base import BaseCommand, CommandError
from apps.bcpp_dispatch.classes import BcppPrepareNetbook


logger = logging.getLogger(__name__)

'''
for user in User.objects.all():
    if not ApiKey.objects.filter(user=user):
        api_key_new = ApiKey.objects.create(user=user)
        api_key_server = ApiKey.objects.using('server').get(user=user)
        api_key_new.key = api_key_server.key
        api_key_new.save()
'''


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<source> <destination>'
    help = 'Prepares netbook for dispatch.'

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError('Missing \'using\' parameters.')
        source = args[0]
        destination = args[1]
        step = 0
        if len(args) == 3:
            step = args[2]
        prepare_netbook = BcppPrepareNetbook(source,
                                                destination,
                                                exception=CommandError,
                                                preparing_netbook=True)
        prepare_netbook.prepare(step=step)
