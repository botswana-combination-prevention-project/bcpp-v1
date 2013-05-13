from django.db.models.signals import post_save
from django.dispatch import receiver
from base_off_study import BaseOffStudy


@receiver(post_save, weak=False, dispatch_uid="base_off_study_post_save")
def base_off_study_post_save(sender, instance, **kwargs):
    """Calls post_save method."""
    if isinstance(instance, BaseOffStudy):
        instance.post_save_clear_future_appointments()
