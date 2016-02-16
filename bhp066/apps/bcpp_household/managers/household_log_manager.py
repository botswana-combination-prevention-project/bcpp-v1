from datetime import timedelta

from django.conf import settings
from django.db import models

from edc.map.classes import site_mappers

from ..classes import PlotIdentifier

from .base_household_structure_manager import BaseHouseholdStructureManager


class HouseholdLogManager(BaseHouseholdStructureManager):
    pass


class HouseholdLogEntryManager(models.Manager):

    def get_by_natural_key(self, report_datetime, household_identifier, survey_name):
        HouseholdLog = models.get_model('bcpp_household', 'HouseholdLog')
        household_log = HouseholdLog.objects.get_by_natural_key(household_identifier, survey_name)
        margin = timedelta(microseconds=999)
        return self.get(report_datetime__range=(
            report_datetime - margin, report_datetime + margin),
            household_log=household_log)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            if PlotIdentifier.get_notebook_plot_lists():
                plot_identifier_list = PlotIdentifier.get_notebook_plot_lists()
                return super(HouseholdLogEntryManager, self).get_queryset().filter(
                    household_log__household_structure__household__plot__community=community,
                    household_log__household_structure__household__plot__plot_identifier__in=plot_identifier_list
                )
            else:
                return super(HouseholdLogEntryManager, self).get_queryset().filter(
                    household_log__household_structure__household__plot__community=community
                )
        return super(HouseholdLogEntryManager, self).get_queryset()
