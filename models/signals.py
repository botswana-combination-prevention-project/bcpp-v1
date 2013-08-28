from django.db.models.signals import post_save
from django.dispatch import receiver
from base_subject import BaseSubject


@receiver(post_save, weak=False, dispatch_uid='base_subject_get_or_create_registered_subject_on_post_save')
def base_subject_get_or_create_registered_subject_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, (BaseSubject, )) and not sender._meta.object_name.lower() == 'registeredsubject':
        registered_subject = instance.post_save_get_or_create_registered_subject()
        try:
            if not instance.registered_subject:
                instance.registered_subject = registered_subject
        except:
            pass
