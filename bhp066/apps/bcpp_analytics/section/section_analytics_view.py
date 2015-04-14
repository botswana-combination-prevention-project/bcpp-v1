from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers


site_mappers.autodiscover()


class SectionAnalyticsView(BaseSectionView):
    section_name = 'Analytics'
    section_display_name = 'Analytics'
    section_display_index = 70
    section_template = 'bcpp_analytics/analytics_index.html'
    #search = {'word': MemberSearchByWord}

    def contribute_to_context(self, context, request, *args, **kwargs):
#         current_survey = None
#         if settings.CURRENT_SURVEY:
#             current_survey = Survey.objects.current_survey()
        context.update({})
        return context

site_sections.register(SectionAnalyticsView)
