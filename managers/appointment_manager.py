from django.db import models
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition


class AppointmentManager(models.Manager):

    def get_by_natural_key(self, visit_instance, code, identity, first_name, dob, initials, registration_identifier, subject_identifier):
        registered_subject = RegisteredSubject.objects.get(
            identity=identity,
            first_name=first_name,
            dob=dob,
            initials=initials,
            registration_identifier=registration_identifier,
            subject_identifier=subject_identifier
            )

        visit_definition = VisitDefinition.objects.get(code=code)
        return self.get(
            registered_subject=registered_subject,
            visit_definition=visit_definition,
            visit_instance=visit_instance
            )
