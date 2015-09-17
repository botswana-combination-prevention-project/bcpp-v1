from copy import deepcopy

from django.conf import settings

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers
from edc.device.device.classes import Device

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_survey.models import Survey

from ..search import SubjectSearchByWord


class SectionSubjectView(BaseSectionView):
    section_name = 'subject'
    section_display_name = 'BHS Subjects'
    section_display_index = 40
    section_template = 'section_bcpp_subject.html'
    dashboard_url_name = 'subject_dashboard_url'
    search = {'word': SubjectSearchByWord}

    def contribute_to_context(self, context, request, *args, **kwargs):
        current_survey = None
        if settings.CURRENT_SURVEY:
            current_survey = Survey.objects.current_survey()
        context.update({
            'current_survey': current_survey,
            'current_community': str(site_mappers.current_mapper()),
            'mapper_name': site_mappers.current_mapper.map_area,
            'subject_dashboard_url': self.dashboard_url_name,
        })
        context.update()
        return context

    def _paginate(self, search_result, page, results_per_page=None):
        """Paginates the search result queryset after which templates
        access search_result.object_list.

        Also sets the 'magic_url' for previous/next paging urls

        Keyword Arguments:
            results_per_page: (default: 25)
        """
        if Device().is_central_server:
            _search_result = []
            if not (settings.LIMIT_EDIT_TO_CURRENT_SURVEY and settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY and settings.FILTERED_DEFAULT_SEARCH):
                for subject_consent in search_result:
                    for household_member in HouseholdMember.objects.filter(registered_subject=subject_consent.household_member.registered_subject):
                        if [survey for survey in Survey.objects.all() if survey == household_member.household_structure.survey]:
                            subject_consent.household_member = household_member
                            subject_consent.survey = household_member.household_structure.survey
                        _search_result.append(deepcopy(subject_consent))
                return super(SectionSubjectView, self)._paginate(_search_result, page, results_per_page)
        else:
            _search_result = []
            for subject_consent in search_result:
                for household_member in HouseholdMember.objects.filter(registered_subject=subject_consent.household_member.registered_subject):
                    if household_member.household_structure.survey.survey_slug == settings.CURRENT_SURVEY:
                        subject_consent.household_member = household_member
                        subject_consent.survey = household_member.household_structure.survey
                        _search_result.append(deepcopy(subject_consent))
            return super(SectionSubjectView, self)._paginate(_search_result, page, results_per_page)

site_sections.register(SectionSubjectView)
