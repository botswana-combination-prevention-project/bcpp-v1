from django.db.models.signals import post_save
from django.dispatch import receiver
from lab_tracker.classes import lab_tracker


@receiver(post_save, weak=False, dispatch_uid="tracker_on_post_save")
def tracker_on_post_save(sender, instance, **kwargs):
    for lab_tracker_cls in lab_tracker.itervalues():
        if sender in lab_tracker_cls.models:
            lab_tracker_cls.update_with_tracker_instance(instance)
