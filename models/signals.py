from django.db.models.signals import post_delete
from django.dispatch import receiver
from bhp_appointment.models import Appointment
from base_registered_subject_model import BaseRegisteredSubjectModel


@receiver(post_delete, weak=False, dispatch_uid='delete_unused_appointments')
def delete_unused_appointments(sender, instance, **kwargs):
    """ Delete unused appointments linked to this instance on delete """
    if isinstance(instance, BaseRegisteredSubjectModel):
        Appointment.objects.delete_appointments_for_instance(instance)