from django.db.models.signals import post_save
from django.dispatch import receiver
from base_appointment_helper_model import BaseAppointmentHelperModel


@receiver(post_save, weak=False, dispatch_uid="prepare_appointments_on_post_save")
def prepare_appointments_on_post_save(sender, instance, **kwargs):
    """"""
    if issubclass(sender, BaseAppointmentHelperModel):
        instance.prepare_appointments()
