from django.db import models
#from bhp_visit.models import VisitDefinition
#from bhp_registration.models import RegisteredSubject


class AppointmentManager(models.Manager):

    def get_by_natural_key(self, visit_instance, code, identity, first_name, dob, initials, subject_identifier):
        return self.get(
            registered_subject__identity=identity,
            registered_subject__first_name=first_name,
            registered_subject__dob=dob,
            registered_subject__initials=initials,
            registered_subject__subject_identifier=subject_identifier,
            visit_definition__code=code,
            visit_instance=visit_instance
            )
