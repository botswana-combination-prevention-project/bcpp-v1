from django.db import models
import dateutil.parser
from datetime import timedelta


class HouseholdLogManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        Household = models.get_model('bcpp_household', 'Household')
        household = Household.objects.get_by_natural_key(household_identifier)
        return self.get(household=household, survey__survey_name=survey_name)


class HouseholdLogEntryManager(models.Manager):

    def get_by_natural_key(self, report_datetime, household_identifier, survey_name):
        HouseholdLog = models.get_model('bcpp_household', 'HouseholdLog')
        household_log = HouseholdLog.objects.get_by_natural_key(household_identifier, survey_name)
        report_datetime = dateutil.parser.parse(report_datetime)
        margin = timedelta(microseconds=999)
        return self.get(report_datetime__range=(report_datetime - margin, report_datetime + margin), household_log=household_log)
