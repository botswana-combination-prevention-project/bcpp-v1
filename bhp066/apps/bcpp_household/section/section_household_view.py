from django.conf import settings

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers

from apps.bcpp_survey.models import Survey
from apps.bcpp_household.constants import CONFIRMED

from ..search import HouseholdSearchByWord


site_mappers.autodiscover()


class SectionHouseholdView(BaseSectionView):
    section_name = 'household'
    section_display_name = 'Households'
    section_display_index = 20
    section_template = 'section_bcpp_household.html'
    dashboard_url_name = 'household_dashboard_url'
    search = {'word': HouseholdSearchByWord}

    def contribute_to_context(self, context, request, *args, **kwargs):
        current_survey = None
        if settings.CURRENT_SURVEY:
            current_survey = Survey.objects.current_survey()
        context.update({
            'current_survey': current_survey,
            'current_community': str(site_mappers.current_mapper()),
            'mapper_name': site_mappers.current_mapper.map_area,
            'CONFIRMED': CONFIRMED})
        return context

site_sections.register(SectionHouseholdView)
