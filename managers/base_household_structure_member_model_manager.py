import dateutil.parser
from datetime import timedelta
from django.db import models


class BaseHouseholdStructureMemberModelManager(models.Manager):

    def get_by_natural_key(self, report_datetime, household_identifier, survey_name, subject_identifier_as_pk):
        # deserialized date follows ECMA-262 specification which has less precision than that reported by mysql
        report_datetime = dateutil.parser.parse(report_datetime)
        margin = timedelta(microseconds=999)
        HouseholdStructureMember = models.get_model('mochudi_household', 'HouseholdStructureMember')
        household_structure_member = HouseholdStructureMember.objects.get_by_natural_key(household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(report_datetime__range=(report_datetime - margin, report_datetime + margin), household_structure_member=household_structure_member)
