from edc.device.sync.management.commands.consume import Command as BaseCommand

from ...classes import BcppConsumer


class Command(BaseCommand):

    @property
    def consumer(self):
        return BcppConsumer()
