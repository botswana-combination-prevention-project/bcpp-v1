from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_subject.constants import POC_VIRAL_LOAD, VIRAL_LOAD
from edc_constants.constants import YES

from bhp066.apps.bcpp_lab.models import PreOrder
from bhp066.apps.bcpp_lab.models import SubjectRequisition


class Command(BaseCommand):

    args = '<community name e.g letlhakeng>'
    help = 'Clean pre-order data.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'community\' parameters.')
        community_name = args[0]
        PreOrder.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community=community_name,
            aliquot_identifier__isnull=True).delete()
        poc_vl_pre_orders_with_aliquote_id = PreOrder.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community=community_name,
            panel__name=POC_VIRAL_LOAD,
            aliquot_identifier__isnull=False)
        total_pre_oders = poc_vl_pre_orders_with_aliquote_id.count()
        count = 0
        for pre_order in poc_vl_pre_orders_with_aliquote_id:
                pre_order.save()
                count += 1
                print(count, " of ", total_pre_oders)
        subject_requisitions = SubjectRequisition.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community=community_name,
            is_drawn=YES,
            panel__name=VIRAL_LOAD)
        total_subject_requisitions = subject_requisitions.count()
        count = 0
        for subject_requisition in subject_requisitions:
            subject_requisition.create_preorder_for_panels(subject_requisition)
            count += 1
            print(count, " of ", total_subject_requisitions)
