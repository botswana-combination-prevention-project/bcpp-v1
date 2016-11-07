from datetime import timedelta

from django.apps import apps as django_apps
from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class SubjectUndecidedEntryManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = ['subject_undecided', 'household_member', 'household_structure', 'household', 'plot']

    def get_by_natural_key(self, report_datetime, household_identifier, survey_name, subject_identifier_as_pk):
        margin = timedelta(microseconds=999)
        SubjectUndecided = django_apps.get_model('bcpp_household_member', 'SubjectUndecided')
        subject_undecided = SubjectUndecided.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(report_datetime__range=(report_datetime - margin, report_datetime + margin),
                        subject_undecided=subject_undecided)
