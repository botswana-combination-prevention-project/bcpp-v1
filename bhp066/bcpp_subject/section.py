from edc.dashboard.section.classes import BaseSectionForDashboardView, site_sections


class SectionSubjectView(BaseSectionForDashboardView):
    section_name = 'subject'
    section_display_name = 'Subjects'
    section_display_index = 30
    section_template = 'section_subject.html'
    dashboard_url_name = 'subject_dashboard_url'

site_sections.register(SectionSubjectView)
