from bhp_section.classes import BaseSectionView, site_sections
from bhp_map.classes import site_mappers


site_mappers.autodiscover()


class SectionExportView(BaseSectionView):
    section_name = 'export'
    section_display_name = 'Import/Export'
    section_display_index = 40
    section_template = 'section_bcpp_exim.html'

site_sections.register(SectionExportView)
