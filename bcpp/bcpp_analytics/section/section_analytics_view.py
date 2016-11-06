from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc_map.site_mappers import site_mappers


site_mappers.autodiscover()


class SectionAnalyticsView(BaseSectionView):
    section_name = 'Analytics'
    section_display_name = 'Analytics'
    section_display_index = 70
    section_template = 'bcpp_analytics/analytics_index.html'

    def contribute_to_context(self, context, request, *args, **kwargs):
        context.update({})
        return context

site_sections.register(SectionAnalyticsView)
