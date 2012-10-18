from django.db.models.signals import post_save
from django.dispatch import receiver
from lab_tracker.classes import tracker


@receiver(post_save, weak=False, dispatch_uid="tracker_on_post_save")
def tracker_on_post_save(sender, instance, **kwargs):
    for model, history_cls in tracker.iteritems():
        if sender == model:
            history_cls.update(sender._meta.object_name)
