import dateutil.parser
from datetime import timedelta
from django.db import models


class BaseRegisteredHouseholdMemberModelManager(models.Manager):

    def get_by_natural_key(self, report_datetime, household_identifier, survey_name, subject_identifier_as_pk):
        report_datetime = dateutil.parser.parse(report_datetime)
        margin = timedelta(microseconds=999)
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(report_datetime__range=(report_datetime - margin, report_datetime + margin),
                        household_member=household_member)
