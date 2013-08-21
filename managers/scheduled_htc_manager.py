from django.db import models


class ScheduledHtcManager(models.Manager):
    """Manager for all scheduled htc models (those with a htc_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        HtcVisit = models.get_model('bcpp_subject', 'HtcVisit')
        htc_visit = HtcVisit.objects.get_by_natural_key(report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(htc_visit=htc_visit)
