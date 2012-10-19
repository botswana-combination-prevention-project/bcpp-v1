from django.db.models.signals import post_save
from django.dispatch import receiver
from lab_tracker.classes import tracker


@receiver(post_save, weak=False, dispatch_uid="tracker_on_post_save")
def tracker_on_post_save(sender, instance, **kwargs):
    for tpl in tracker.itervalues():
        model_cls, history_cls = tpl
        if sender == model_cls:
            history_cls.update_for_instance(instance)
