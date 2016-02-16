from django.conf import settings

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers

site_mappers.autodiscover()


class SectionReportsView(BaseSectionView):
    section_name = 'reports'
    section_display_name = 'Reports'
    section_display_index = 50
    section_template = 'section_bcpp_reports.html'

    def contribute_to_context(self, context, request, *args, **kwargs):
        return context

    def get_current_community(self):
        return site_mappers.get_mapper(site_mappers.current_community).map_area

site_sections.register(SectionReportsView)
