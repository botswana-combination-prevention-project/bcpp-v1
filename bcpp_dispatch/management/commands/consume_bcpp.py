from bhp_sync.management.commands.consume import Command as BaseCommand
from bcpp_dispatch.classes import BcppConsumer


class Command(BaseCommand):

    def get_consumer(self):
        return BcppConsumer()
