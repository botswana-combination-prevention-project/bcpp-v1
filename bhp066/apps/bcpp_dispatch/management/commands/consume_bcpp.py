from edc.device.sync.management.commands.consume import Command as BaseCommand
from apps.bcpp_dispatch.classes import BcppConsumer


class Command(BaseCommand):

    def get_consumer(self):
        return BcppConsumer()
