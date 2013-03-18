from django.db import models
from bhp_appointment.models import Appointment


class BaseVisitTrackingManager(models.Manager):
    def get_by_natural_key(self, visit_instance, visit_definition_code, identity, first_name, dob, initials, subject_identifier):
        appointment = Appointment.objects.get_by_natural_key(visit_instance, visit_definition_code, identity, first_name, dob, initials, subject_identifier)
        return self.get(appointment=appointment)
