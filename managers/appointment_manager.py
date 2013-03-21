from django.db import models
#from bhp_visit.models import VisitDefinition
#from bhp_registration.models import RegisteredSubject


class AppointmentManager(models.Manager):

    def get_by_natural_key(self, visit_instance, appt_status, code, subject_identifier):
        return self.get(
            registered_subject__subject_identifier=subject_identifier,
            visit_definition__code=code,
            visit_instance=visit_instance,
            appt_status=appt_status,
            )
