from django.db.models.signals import post_save
from django.dispatch import receiver
from pre_appointment_contact import PreAppointmentContact


@receiver(post_save, weak=False, dispatch_uid="PreAppointmentContact_on_post_save")
def PreAppointmentContact_on_post_save(sender, instance, **kwargs):
    """Calls post_save method which will only call save."""
    if isinstance(instance, PreAppointmentContact):
        instance.post_save()
