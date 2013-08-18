from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from bhp_lab_tracker.classes import site_lab_tracker


@receiver(post_save, weak=False, dispatch_uid="tracker_on_post_save")
def tracker_on_post_save(sender, instance, **kwargs):
    """Updates the tracker on pos-save for models registered in lab_tracker."""
    if site_lab_tracker.autodiscovered:
        if isinstance(instance, site_lab_tracker.get_model_list()):
            site_lab_tracker.update(instance)


@receiver(post_delete, weak=False, dispatch_uid="tracker_on_post_delete")
def tracker_on_post_delete(sender, instance, **kwargs):
    """Deletes the tracker on post-delete for models registered in lab_tracker."""
    if site_lab_tracker.autodiscovered:
        if isinstance(instance, site_lab_tracker.get_model_list()):
            site_lab_tracker.delete_history(instance)
