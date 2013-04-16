from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pre_appointment_contact import PreAppointmentContact


@receiver(post_save, weak=False, dispatch_uid="pre_appointment_contact_on_post_save")
def pre_appointment_contact_on_post_save(sender, instance, **kwargs):
    """Calls post_save method which will only call save."""
    if isinstance(instance, PreAppointmentContact):
        instance.post_save()


@receiver(post_delete, weak=False, dispatch_uid="pre_appointment_contact_on_post_delete")
def pre_appointment_contact_on_post_delete(sender, instance, **kwargs):
    """Calls post_delete method."""
    if isinstance(instance, PreAppointmentContact):
        instance.post_delete()
