from django.conf import settings

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers
from edc_device import device

from bhp066.apps.bcpp_survey.models import Survey

from ..constants import CONFIRMED
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
            'current_community': str(site_mappers.get_current_mapper()),
            'mapper_name': site_mappers.get_current_mapper().map_area,
            'CONFIRMED': CONFIRMED})
        return context

    def _paginate(self, search_result, page, results_per_page=None):
        """
        Filters the search result based on whether the device is a central_server or other devices. if central server
        then for baseline year it returns only baseline results, for annual then returns baseline and annual results
        and for third year returns all search results.

        Paginates the search result queryset after which templates
        access search_result.object_list.

        Also sets the 'magic_url' for previous/next paging urls

        Keyword Arguments:
            results_per_page: (default: 25)
        """
        current_survey = Survey.objects.current_survey()
        if not results_per_page:
            results_per_page = 25
        if device.is_central_server:
            if current_survey.survey_abbrev == 'Y1':
                _search_result = []
                for household_structure in search_result:
                    if household_structure.survey.survey_abbrev == 'Y1':
                        _search_result.append(household_structure)
                return super(SectionHouseholdView, self)._paginate(_search_result, page, results_per_page)
            elif current_survey.survey_abbrev == 'Y2':
                _search_result = []
                for household_structure in search_result:
                    if household_structure.survey.survey_abbrev in ['Y1', 'Y2']:
                        _search_result.append(household_structure)
                return super(SectionHouseholdView, self)._paginate(_search_result, page, results_per_page)
            else:
                return super(SectionHouseholdView, self)._paginate(search_result, page, results_per_page)
        else:
            _search_result = []
            for household_structure in search_result:
                if household_structure.survey == current_survey:
                    _search_result.append(household_structure)
            return super(SectionHouseholdView, self)._paginate(_search_result, page, results_per_page)

site_sections.register(SectionHouseholdView)
