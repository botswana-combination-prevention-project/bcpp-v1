from optparse import make_option
from django.db.models import Count
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from bhp_sync.models import IncomingTransaction
from bhp_lab_tracker.classes import lab_tracker

lab_tracker.autodiscover()


class Command(BaseCommand):

    args = ()
    help = 'Print uncomsumed incoming transactions breakdown by tx_name. '

    def handle(self, *args, **options):
        if not args:
            args = [None]
        stats = self.prepare_stats()
        self.prepare_stats(stats)
        

    def prepare_stats(self):
        return IncomingTransaction.objects.values('tx_name').filter(is_consumed=False,is_ignored=False).annotate(tx_count=Count('tx_name'))
        
    def print_stats (self, stats):
        print "Total:\t:Transaction name"

        for stat in stats:
            print "{0}\t:{1}".format(stat['tx_count'],stat['tx_name'])

