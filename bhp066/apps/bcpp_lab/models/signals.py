from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bcpp_subject.classes import func_poc_vl
from apps.bcpp_subject.constants import CLOSED, VIRAL_LOAD, ARBIT_VIRAL_LOAD, POC_VIRAL_LOAD

from ..models import ClinicRequisition, SubjectRequisition, PreOrder, Panel, Order
from django.db import transaction


@receiver(post_save, weak=False, dispatch_uid="clinic_requisition_on_post_save")
def clinic_requisition_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, ClinicRequisition):
            instance.change_metadata_status_on_post_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="requisition_not_drawn")
def requisition_not_drawn(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, ClinicRequisition):
            instance.requisition_not_drawn()


@receiver(post_save, weak=False, dispatch_uid="create_requisition_preorder_on_post_save")
def create_requisition_preorder_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, SubjectRequisition):
            with transaction.atomic():
                if instance.panel.name == VIRAL_LOAD and func_poc_vl(instance.subject_visit):
                    poc_viral_load = Panel.objects.get(name=POC_VIRAL_LOAD)
                    arbit_viral_load = Panel.objects.get(name=ARBIT_VIRAL_LOAD)
                    PreOrder.objects.create(panel=poc_viral_load, preorder_datetime=datetime.now(), subject_identifier=instance.subject_identifier)
                    PreOrder.objects.create(panel=arbit_viral_load, preorder_datetime=datetime.now(), subject_identifier=instance.subject_identifier)
                else:
                    PreOrder.objects.create(panel=instance.panel, preorder_datetime=datetime.now(), subject_identifier=instance.subject_identifier)


@receiver(post_save, weak=False, dispatch_uid="create_order_on_pre_save")
def create_order_on_pre_save(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, PreOrder) and instance.status == CLOSED:
            pass