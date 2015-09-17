from django.db import models
from django.conf import settings

from edc.map.classes import site_mappers

from ..classes import PlotIdentifier


class BaseHouseholdStructureManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        HouseholdStructure = models.get_model('bcpp_household', 'HouseholdStructure')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        return self.get(household_structure=household_structure)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.current_mapper.map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(BaseHouseholdStructureManager, self).get_queryset().filter(
                    household_structure__household__plot__community=community,
                    household_structure__household__plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists()
                    )
            else:
                return super(BaseHouseholdStructureManager, self).get_queryset().filter(
                    household_structure__household__plot__community=community
                    )
        return super(BaseHouseholdStructureManager, self).get_queryset()
