from bhp_section.classes import BaseSectionView, site_sections


class SectionSubjectView(BaseSectionView):
    section_name = 'subject'
    section_display_name = 'Subjects'
    section_display_index = 20
    section_template = 'section_subject.html'
    dashboard_url_name = 'subject_dashboard_url'
site_sections.register(SectionSubjectView)
