from django.db.models.signals import post_save
from django.dispatch import receiver
from base_subject import BaseSubject


@receiver(post_save, weak=False, dispatch_uid='base_subject_on_post_save')
def base_subject_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, (BaseSubject)):
        instance.post_save_get_or_create_registered_subject()
