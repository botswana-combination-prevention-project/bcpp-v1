from django.conf import settings

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers

from apps.bcpp_survey.models import Survey

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
        return context

site_sections.register(SectionSubjectView)
