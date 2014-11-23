from edc.dashboard.section.classes import BaseSectionForDashboardView, site_sections

from ..search import SubjectSearchByWord


class SectionSubjectView(BaseSectionForDashboardView):
    section_name = 'subject'
    section_display_name = 'BHS Subjects'
    section_display_index = 40
    section_template = 'section_bcpp_subject.html'
    dashboard_url_name = 'subject_dashboard_url'
    search = {'word': SubjectSearchByWord}
site_sections.register(SectionSubjectView)
