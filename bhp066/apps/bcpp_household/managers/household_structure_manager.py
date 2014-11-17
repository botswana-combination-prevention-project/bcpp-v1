from django.db import models

from apps.bcpp_survey.models import Survey


class HouseholdStructureManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        survey = Survey.objects.get_by_natural_key(survey_name)
        Household = models.get_model('bcpp_household', 'Household')
        household = Household.objects.get_by_natural_key(household_identifier)
        return self.get(household=household, survey=survey)

    def fetch_household_members(self, household, source_survey, target_survey):
        """Gets (or creates) members for the given household structure."""
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        source_household_structure = self.get(household=household, survey=source_survey)
        try:
            target_household_structure = self.get(household=household, survey=target_survey, enumerated=False)
            for household_member in HouseholdMember.object.filter(household_structure=source_household_structure):
                options = dict(
                    household_structure=target_household_structure,
                    first_name=household_member.first_name,
                    initials=household_member.initials,
                    age_in_years=household_member.age_in_years,
                    gender=household_member.gender,
                    relation=household_member.relation,
                    inability_to_participate=household_member.inability_to_participate,
                    internal_identifier=household_member.internal_identifier,
                    )
                HouseholdMember.object.create(**options)
            target_household_structure.enumerated = False
            target_household_structure.save(update_fields=['enumerated'])
        except self.model.DoesNotExist:
            pass
