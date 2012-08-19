from django.db.models.signals import post_save
from django.dispatch import receiver
from lab_longitudinal.classes import longitudinal_history


@receiver(post_save, weak=False, dispatch_uid="longitudinal_on_post_save")
def longitudinal_on_post_save(sender, instance, **kwargs):
    for model, history_cls in longitudinal_history.iteritems():
        if sender == model:
            history_cls.update(sender._meta.object_name)
