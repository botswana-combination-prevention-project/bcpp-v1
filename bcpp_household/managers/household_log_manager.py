from datetime import timedelta

from django.apps import apps as django_apps
from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin

from .manager_mixins import HouseholdStructureManagerMixin


class HouseholdLogManager(CurrentCommunityManagerMixin, HouseholdStructureManagerMixin, models.Manager):

    lookup = 'household_structure__household__plot'


class HouseholdLogEntryManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = 'household_log__household_structure__household__plot'

    def get_by_natural_key(self, report_datetime, household_identifier, survey_name):
        HouseholdLog = django_apps.get_model('bcpp_household', 'HouseholdLog')
        household_log = HouseholdLog.objects.get_by_natural_key(household_identifier, survey_name)
        margin = timedelta(microseconds=999)
        return self.get(report_datetime__range=(
            report_datetime - margin, report_datetime + margin),
            household_log=household_log)
