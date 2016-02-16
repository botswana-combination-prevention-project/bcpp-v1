from django.conf import settings
from django.db import models

from edc.map.classes import site_mappers

from ..classes import PlotIdentifier


class HouseholdManager(models.Manager):

    def get_by_natural_key(self, household_identifier):
        return self.get(household_identifier=household_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(HouseholdManager, self).get_queryset().filter(
                    plot__community=community,
                    plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists())
            else:
                return super(HouseholdManager, self).get_queryset().filter(plot__community=community)
        return super(HouseholdManager, self).get_queryset()
