from django.db.models.signals import post_save
from django.dispatch import receiver
from base_visit_tracking import BaseVisitTracking
from bhp_entry.classes import ScheduledEntry


@receiver(post_save, weak=False, dispatch_uid="base_visit_tracking_check_in_progress_on_post_save")
def base_visit_tracking_check_in_progress_on_post_save(sender, instance, **kwargs):
    """Calls post_save method on the visit tracking instance."""
    if isinstance(instance, BaseVisitTracking):
        instance.post_save_check_in_progress()


@receiver(post_save, weak=False, dispatch_uid="base_visit_tracking_add_or_update_entry_buckets_on_post_save")
def base_visit_tracking_add_or_update_entry_buckets_on_post_save(sender, instance, **kwargs):
    """ Adds missing bucket entries and flags added and existing entries as keyed or not keyed (only)."""
    if isinstance(instance, BaseVisitTracking):
        scheduled_entry = ScheduledEntry()
        scheduled_entry.add_or_update_for_visit(instance)
