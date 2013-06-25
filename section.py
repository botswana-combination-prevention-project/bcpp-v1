from bhp_section.classes import BaseSectionView, site_sections
from models import SubjectConsent


class SectionSubjectView(BaseSectionView):
    section_name = 'subject'
    section_display_name = 'Subjects'
    section_display_index = 20
    section_template = 'section_subject.html'
    add_model = SubjectConsent

site_sections.register(SectionSubjectView)
