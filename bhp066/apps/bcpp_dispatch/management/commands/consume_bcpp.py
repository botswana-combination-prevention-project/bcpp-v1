from edc.device.sync.management.commands.consume import Command as BaseCommand

from bhp066.apps.bcpp_dispatch.classes import BcppConsumer


class Command(BaseCommand):
    """A management command to consume incoming transactions for BCPP."""
    @property
    def consumer(self):
        """Returns an instance of BCPP specific incoming transaction consumer."""
        return BcppConsumer()
