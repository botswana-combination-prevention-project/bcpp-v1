from django.db.models.signals import post_save
from django.dispatch import receiver
from bhp_lab_tracker.classes import lab_tracker


@receiver(post_save, weak=False, dispatch_uid="tracker_on_post_save")
def tracker_on_post_save(sender, instance, **kwargs):
    for lab_tracker_cls in lab_tracker.all():
        for model_tpl in lab_tracker_cls().models:
            if sender in model_tpl:
                lab_tracker_cls().update_with_tracker_instance(instance, model_tpl)
