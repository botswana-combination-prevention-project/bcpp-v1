from edc.device.sync.management.commands.consume import Command as BaseCommand
from ...classes import ClinicBcppConsumer


class Command(BaseCommand):

    def get_consumer(self):
        return ClinicBcppConsumer()
