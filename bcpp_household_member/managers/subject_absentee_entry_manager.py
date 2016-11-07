from datetime import timedelta

from django.apps import apps as django_apps
from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class SubjectAbsenteeEntryManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = ['subject_absentee', 'household_member', 'household_structure', 'household', 'plot']

    def get_by_natural_key(self, report_datetime, household_identifier, survey_name, subject_identifier_as_pk):
        margin = timedelta(microseconds=999)
        SubjectAbsentee = django_apps.get_model('bcpp_household_member', 'SubjectAbsentee')
        subject_absentee = SubjectAbsentee.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(report_datetime__range=(report_datetime - margin, report_datetime + margin),
                        subject_absentee=subject_absentee)
