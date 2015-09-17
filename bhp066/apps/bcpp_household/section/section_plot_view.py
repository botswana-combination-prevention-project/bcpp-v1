from django.conf import settings

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers

from bhp066.apps.bcpp_survey.models import Survey

from ..forms import GpsSearchForm
from ..search import PlotSearchByWord

site_mappers.autodiscover()


class SectionPlotView(BaseSectionView):
    section_name = 'plot'
    section_display_name = 'Plots'
    section_display_index = 10
    section_template = 'section_bcpp_plot.html'
    search = {'word': PlotSearchByWord}
    show_most_recent = False

    def contribute_to_context(self, context, request, *args, **kwargs):
        current_survey = None
        if settings.CURRENT_SURVEY:
            current_survey = Survey.objects.current_survey()
        context.update({
            'current_survey': current_survey,
            'current_community': str(site_mappers.current_mapper()),
            'mapper_name': site_mappers.current_mapper.map_area,
            'gps_search_form': GpsSearchForm(initial={'radius': 100}),
            'use_gps_to_target_verification': settings.VERIFY_GPS,
            'search_term': kwargs.get('search_term'),
        })
        context.update()
        return context

    def get_current_community(self):
        return site_mappers.get_current_mapper().map_area

site_sections.register(SectionPlotView)
