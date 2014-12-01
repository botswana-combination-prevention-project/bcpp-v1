from django.db import models

from apps.bcpp_survey.models import Survey
from apps.bcpp_household_member.classes.enumeration_helper import EnumerationHelper


class HouseholdStructureManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        survey = Survey.objects.get_by_natural_key(survey_name)
        Household = models.get_model('bcpp_household', 'Household')
        household = Household.objects.get_by_natural_key(household_identifier)
        return self.get(household=household, survey=survey)

    def add_household_members_from_survey(self, household, source_survey, target_survey):
        """Adds household members from a previous survey to an
        unenumerated household structure of a new survey."""
        enumeration_helper = EnumerationHelper(household, source_survey, target_survey)
        return enumeration_helper.add_members_from_survey()
