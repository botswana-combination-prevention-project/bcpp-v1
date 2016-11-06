from django.conf import settings

from edc_map.site_mappers import site_mappers
from edc_consent.managers import ConsentManager

from bcpp_household.plot_identifier import PlotIdentifier


class SubjectConsentManager(ConsentManager):

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            nt_ls = PlotIdentifier.get_notebook_plot_lists()
            if PlotIdentifier.get_notebook_plot_lists():
                return super(
                    SubjectConsentManager, self).get_queryset().filter(
                        community=community,
                        household_member__household_structure__household__plot__plot_identifier__in=nt_ls)
            else:
                return super(SubjectConsentManager, self).get_queryset().filter(community=community)
        return super(SubjectConsentManager, self).get_queryset()
