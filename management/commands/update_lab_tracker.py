import logging
from django.core.management.base import BaseCommand
from bhp_lab_tracker.classes import site_lab_tracker

site_lab_tracker.autodiscover()
logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Command(BaseCommand):

    args = ()
    help = 'Update bhp_lab_tracker history model.'

    def handle(self, *args, **options):
        site_lab_tracker.update_all(False)
