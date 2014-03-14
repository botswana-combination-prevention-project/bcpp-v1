from django.db import models

from apps.bcpp_survey.models import Survey


class HouseholdStructureManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        survey = Survey.objects.get_by_natural_key(survey_name)
        Household = models.get_model('bcpp_household', 'Household')
        household = Household.objects.get_by_natural_key(household_identifier)
        return self.get(household=household, survey=survey)

    def fetch_household_members(self, household_structure):
        """Gets (or creates) members for the given household structure.

        .. note:: this calls for the members from the household dashboard."""
        from apps.bcpp_dashboard.classes import HouseholdDashboard
        dashboard_type = 'household'
        dashboard_model = 'household_structure'
        dashboard_id = household_structure.pk
        household_dashboard = HouseholdDashboard(dashboard_type, dashboard_id, dashboard_model, survey=household_structure.survey.pk)
        return household_dashboard.household_members
