from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from bhp_lab_tracker.classes import lab_tracker


@receiver(post_save, weak=False, dispatch_uid="tracker_on_post_save")
def tracker_on_post_save(sender, instance, **kwargs):
    """Updates the tracker on pos-save for models registered in lab_tracker."""
    for lab_tracker_cls in lab_tracker.all():
        for model_tpl in lab_tracker_cls().models:
            if sender in model_tpl:
                lab_tracker_cls().update_with_tracker_instance(instance, model_tpl)


@receiver(post_delete, weak=False, dispatch_uid="tracker_on_post_delete")
def tracker_on_post_delete(sender, instance, **kwargs):
    """Deletes the tracker on post-delete for models registered in lab_tracker."""
    for lab_tracker_cls in lab_tracker.all():
        for model_tpl in lab_tracker_cls().models:
            if sender in model_tpl:
                lab_tracker_cls().delete_with_tracker_instance(instance, model_tpl)
