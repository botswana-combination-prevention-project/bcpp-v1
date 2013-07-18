from django.conf import settings
from bhp_section.classes import BaseSectionView, site_sections
from bhp_map.classes import site_mapper
from bcpp_survey.forms import SurveyForm
from models import Household
from forms import CommunityForm


site_mapper.autodiscover()


class SectionHouseholdView(BaseSectionView):
    section_name = 'household'
    section_display_name = 'Households'
    section_display_index = 10
    section_template = 'household_dashboard.html'
    add_model = Household

    def contribute_to_context(self, context):
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
        return context

site_sections.register(SectionHouseholdView)
