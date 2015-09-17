from django.conf import settings
from django.db import models

from edc.map.classes import site_mappers

from bhp066.apps.bcpp_household.classes import PlotIdentifier


class BaseHouseholdMemberManager(models.Manager):
    """Manager base class for managers on models with key to HouseholdMember."""

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk):
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(household_member=household_member)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.current_mapper.map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(BaseHouseholdMemberManager, self).get_queryset().filter(
                    household_member__household_structure__household__plot__community=community,
                    household_member__household_structure__household__plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists()
                    )
            else:
                return super(BaseHouseholdMemberManager, self).get_queryset().filter(
                    household_member__household_structure__household__plot__community=community,)
        return super(BaseHouseholdMemberManager, self).get_queryset()
