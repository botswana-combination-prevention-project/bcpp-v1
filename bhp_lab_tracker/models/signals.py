from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, weak=False, dispatch_uid="tracker_on_post_save")
def tracker_on_post_save(sender, instance, **kwargs):
    """Updates the lab_tracker history on post-save for model instances whose class is registered in site_lab_tracker."""
    from bhp_lab_tracker.classes import site_lab_tracker
    if site_lab_tracker.get_autodiscovered():
        if isinstance(instance, site_lab_tracker.get_model_list()):
            site_lab_tracker.update_history(instance)


@receiver(post_delete, weak=False, dispatch_uid="tracker_on_post_delete")
def tracker_on_post_delete(sender, instance, **kwargs):
    """Deletes from the lab_tracker history for a model instance on post-save for model instances whose class is registered in site_lab_tracker."""
    from bhp_lab_tracker.classes import site_lab_tracker
    if site_lab_tracker.get_autodiscovered():
        if isinstance(instance, site_lab_tracker.get_model_list()):
            site_lab_tracker.delete_history(instance)
