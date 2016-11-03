from edc.dashboard.section.classes import BaseSectionForDashboardView, site_sections


class SectionHtcSubjectView(BaseSectionForDashboardView):
    section_name = 'htc_subject'
    section_display_name = 'HTC Subjects'
    section_display_index = 40
    section_template = 'section_htc_subject.html'

# site_sections.register(SectionHtcSubjectView)
