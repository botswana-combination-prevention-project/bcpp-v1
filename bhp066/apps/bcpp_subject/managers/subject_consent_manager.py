from django.conf import settings

from edc_consent.models import ConsentManager
from edc.map.classes import site_mappers

from bhp066.apps.bcpp_household.classes import PlotIdentifier


class SubjectConsentManager(ConsentManager):

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_current_mapper().map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(
                    SubjectConsentManager, self).get_queryset().filter(
                        community=community,
                        household_member__household_structure__household__plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists())
            else:
                return super(SubjectConsentManager, self).get_queryset().filter(community=community)
        return super(SubjectConsentManager, self).get_queryset()
