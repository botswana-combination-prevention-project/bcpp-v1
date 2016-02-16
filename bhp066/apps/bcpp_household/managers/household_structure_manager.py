from django.db import models
from django.conf import settings

from edc.map.classes import site_mappers

from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household_member.classes import EnumerationHelper

from ..classes import PlotIdentifier


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

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(HouseholdStructureManager, self).get_queryset().filter(
                    household__plot__community=community,
                    household__plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists())
            else:
                return super(HouseholdStructureManager, self).get_queryset().filter(
                    household__plot__community=community)
        return super(HouseholdStructureManager, self).get_queryset()
