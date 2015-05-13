from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import ClinicRequisition


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
