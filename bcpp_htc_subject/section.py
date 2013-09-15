from bhp_section.classes import BaseSectionView, site_sections


class SectionHtcSubjectView(BaseSectionView):
    section_name = 'htc_subject'
    section_display_name = 'HTC Subjects'
    section_display_index = 40
    section_template = 'section_htc_subject.html'

site_sections.register(SectionHtcSubjectView)
