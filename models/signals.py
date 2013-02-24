from django.db.models.signals import post_save
from django.dispatch import receiver
from base_visit_tracking import BaseVisitTracking
from bhp_entry.classes import ScheduledEntry, AdditionalEntry


@receiver(post_save, weak=False, dispatch_uid="base_visit_tracking_on_post_save")
def base_visit_tracking_on_post_save(sender, instance, **kwargs):
    """Calls post_save method on the visit tracking instance."""
    if isinstance(instance, BaseVisitTracking):
        instance.post_save()


@receiver(post_save, weak=False, dispatch_uid="base_visit_tracking_add_or_update_entry_buckets_on_post_save")
def base_visit_tracking_add_or_update_entry_buckets_on_post_save(sender, instance, **kwargs):
    """ Adds missing bucket entries and flags added and existing entries as keyed or not keyed (only)."""
    if isinstance(instance, BaseVisitTracking):
        scheduled_entry = ScheduledEntry()
        scheduled_entry.add_or_update_for_visit(instance)

#        # if requisition_model has been defined, assume scheduled labs otherwise pass
#        if hasattr(self, 'requisition_model'):
#            ScheduledLabEntryBucket.objects.add_for_visit(
#                visit_model_instance=visit_model_instance,
#                requisition_model=self.requisition_model)
#        if instance.registered_subject:
#            additional_entry = AdditionalEntry()
#            additional_entry.update_for_registered_subject(instance.registered_subject)