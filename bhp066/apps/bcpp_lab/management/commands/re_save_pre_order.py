from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_subject.constants import ABBOTT_VIRAL_LOAD, POC_VIRAL_LOAD

from bhp066.apps.bcpp_lab.models import PreOrder


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>'
    help = 'Re save household log entries.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        pre_orders = PreOrder.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community=community_name,
            panel__name__in=[POC_VIRAL_LOAD, ABBOTT_VIRAL_LOAD])
        total_pre_oders = len(pre_orders)
        count = 0
        for pre_order in pre_orders:
                pre_order.save()
                count += 1
                print count, " of ", total_pre_oders
