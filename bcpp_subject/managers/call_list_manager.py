from django.db import models
from django.conf import settings

from edc_map.site_mappers import site_mappers

from bhp066.apps.bcpp_household.classes import PlotIdentifier


class CallListManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk, label):
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(household_member=household_member, label=label)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_current_mapper().map_area
            if PlotIdentifier.get_notebook_plot_lists():
                community = site_mappers.get_current_mapper().map_area
                return super(CallListManager, self).get_queryset().filter(
                    household_member__household_structure__household__plot__community=community,
                    household_member__household_structure__household__plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists())
            else:
                return super(CallListManager, self).get_queryset().filter(
                    household_member__household_structure__household__plot__community=community)
        return super(CallListManager, self).get_queryset()
