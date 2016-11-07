from django.apps import apps as django_apps
from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class ScheduledModelManager(CurrentCommunityManagerMixin, models.Manager):
    """Manager for all scheduled models (those with a subject_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        SubjectVisit = django_apps.get_model('bcpp_subject', 'SubjectVisit')
        subject_visit = SubjectVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, code, subject_identifier_as_pk)
        return self.get(subject_visit=subject_visit)
