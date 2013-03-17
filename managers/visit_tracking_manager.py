from django.db import models
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_appointment.models import Appointment


class VisitTrackingManager(models.Manager):
    def get_by_natural_key(self, visit_instance, visit_definition, identity, first_name, dob, initials, registration_identifier, subject_identifier):
        return self.get(appointment=appointment)
