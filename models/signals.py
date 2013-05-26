from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pre_appointment_contact import PreAppointmentContact
from appointment import Appointment


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

# moved to appointment model file!
# @receiver(post_save, weak=False, dispatch_uid="check_appt_status_on_post_save")
# def check_appt_status_on_post_save(sender, instance, raw, created, using, **kwargs):
#     if isinstance(instance, Appointment):
#         instance.post_save_check_appt_status(created, using)
