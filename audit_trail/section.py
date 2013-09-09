from bhp_section.classes import BaseSectionView, site_sections


class SectionAuditView(BaseSectionView):
    section_name = 'audit_trail'
    section_display_name = 'Audit'
    section_display_index = 130
    # section_template =

site_sections.register(SectionAuditView)
