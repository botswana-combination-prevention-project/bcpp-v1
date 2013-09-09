import logging
from django.core.management.base import BaseCommand
from bhp_lab_tracker.classes import site_lab_tracker
from bhp_lab_tracker.models import HistoryModel


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
        """Update the history model for all registered subjects."""
        cnt = HistoryModel.objects.all().count()
        print 'Starting with {0} records in the History Model.'.format(cnt)
        print '...updating'
        index, tot = site_lab_tracker.update_history_for_all(False)
        print '...done'
        cnt = HistoryModel.objects.all().count()
        print 'Have {0} records in the History Model after update.'.format(cnt)
        print "Updated for {0}/{1} registered subjects".format(index + 1, tot)
