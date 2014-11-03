from django.conf import settings

from edc.dashboard.section.classes import BaseSectionForDashboardView, site_sections
from edc.map.classes import site_mappers

from apps.bcpp_survey.models import Survey
from apps.bcpp_household.constants import CONFIRMED

from ..forms import GpsSearchForm
from ..search import HouseholdSearchByWord, HouseholdSearchByGps


site_mappers.autodiscover()


class SectionHouseholdView(BaseSectionForDashboardView):
    section_name = 'household'
    section_display_name = 'Households'
    section_display_index = 20
    section_template = 'section_bcpp_household.html'
    dashboard_url_name = 'household_dashboard_url'
    search = {'word': HouseholdSearchByWord, 'gps': HouseholdSearchByGps}

    def contribute_to_context(self, context, request, *args, **kwargs):
        current_survey = None
        if settings.CURRENT_SURVEY:
            current_survey = Survey.objects.current_survey()
        context.update({
            'current_survey': current_survey,
            'current_community': str(site_mappers.get_current_mapper()()),
            'mapper_name': site_mappers.get_current_mapper().map_area,
            'gps_search_form': GpsSearchForm(initial={'radius': 100}),
            'CONFIRMED': CONFIRMED})
        return context

    def get_current_community(self):
        return site_mappers.get_current_mapper().map_area

site_sections.register(SectionHouseholdView)
