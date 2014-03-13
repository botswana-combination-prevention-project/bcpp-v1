from django.db import models


class ScheduledRBDModelManager(models.Manager):
    """Manager for all scheduled models (those with a subject_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        SubjectVisitRBD = models.get_model('bcpp_rbd_subject', 'SubjectVisitRBD')
        subject_visit_rbd = SubjectVisitRBD.objects.get_by_natural_key(report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(subject_visit_rbd=subject_visit_rbd)