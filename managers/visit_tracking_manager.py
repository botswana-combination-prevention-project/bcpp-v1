from django.db import models
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_appointment.models import Appointment


class VisitTrackingManager(models.Manager):
    def get_by_natural_key(self, visit_instance, visit_definition, identity, first_name, dob, initials, registration_identifier):
        registered_subject = RegisteredSubject.objects.get(
            identity=identity,
            first_name=first_name,
            dob=dob,
            initials=initials,
            registration_identifier=registration_identifier
            )
        visit_definition = VisitDefinition.objects.get(code=visit_definition)

        appointment = Appointment.objects.get(
            registered_subject=registered_subject,
            visit_definition=visit_definition,
            visit_instance=visit_instance
            )
        return self.get(appointment=appointment)

    def get_by_natural_key_with_dict(self, **kwargs):
        return self.get(**kwargs)
