from django.db import models


class ScheduledModelManager(models.Manager):
    """Manager for all scheduled htc models (those with a htc_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        HtcSubjectVisit = models.get_model('bcpp_htc_subject', 'HtcSubjectVisit')
        htc_subject_visit = HtcSubjectVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(htc_subject_visit=htc_subject_visit)
