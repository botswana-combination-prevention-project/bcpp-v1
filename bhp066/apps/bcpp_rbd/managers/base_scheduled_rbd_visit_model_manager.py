from django.db import models


class ScheduledRBDModelManager(models.Manager):
    """Manager for all scheduled models (those with a subject_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        RBDVisit = models.get_model('bcpp_RBD_subject', 'RBDVisit')
        rbd_visit = RBDVisit.objects.get_by_natural_key(report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(rbd_visit=rbd_visit)