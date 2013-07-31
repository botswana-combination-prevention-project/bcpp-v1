from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bhp_section.classes import BaseSectionView, site_sections
from bhp_map.classes import site_mappers
from bcpp_survey.forms import SurveyForm
from models import Household
from forms import CommunityForm


site_mappers.autodiscover()


class SectionHouseholdView(BaseSectionView):
    section_name = 'household'
    section_display_name = 'Households'
    section_display_index = 10
    section_template = 'section_bcpp_household.html'
    add_model = Household

    def contribute_to_context(self, context, request, *args, **kwargs):
        current_survey = None
        if 'CURRENT_SURVEY' in dir(settings):
            current_survey = settings.CURRENT_SURVEY
            survey_form = None
        else:
            survey_form = SurveyForm()
        context.update({'survey_form': survey_form, 'current_survey': current_survey})
        current_community = None
        if 'CURRENT_COMMUNITY' in dir(settings):
            current_community = settings.CURRENT_COMMUNITY
            community_form = None
        else:
            community_form = CommunityForm()
        context.update({'community_form': community_form, 'current_community': current_community})

        # handle gps search
        # search_result = 
        #search_result = self._paginate(search_result)
        #context.add({'search_result': search_result})
        return context

    def _paginate(self, search_result, page=1, results_per_page=None):
        """Paginates the search result queryset after which templates
        access search_result.object_list.

        Also sets the 'magic_url' for previous/next paging urls

        Keyword Arguments:
            results_per_page: (default: 25)
        """
        if not results_per_page:
            results_per_page = 25
        if search_result:
            paginator = Paginator(search_result, results_per_page)
            try:
                search_result = paginator.page(page)
            except (EmptyPage, InvalidPage):
                search_result = paginator.page(paginator.num_pages)
        return search_result


site_sections.register(SectionHouseholdView)
