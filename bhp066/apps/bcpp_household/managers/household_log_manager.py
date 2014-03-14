import dateutil.parser
from datetime import timedelta
from django.db import models


class HouseholdLogManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        HouseholdStructure = models.get_model('bcpp_household', 'HouseholdStructure')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        return self.get(household_structure=household_structure)


class HouseholdLogEntryManager(models.Manager):

    def get_by_natural_key(self, report_datetime, household_identifier, survey_name):
        HouseholdLog = models.get_model('bcpp_household', 'HouseholdLog')
        household_log = HouseholdLog.objects.get_by_natural_key(household_identifier, survey_name)
        margin = timedelta(microseconds=999)
        return self.get(report_datetime__range=(report_datetime - margin, report_datetime + margin), household_log=household_log)
