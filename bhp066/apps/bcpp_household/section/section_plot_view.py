from django.conf import settings

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers

from apps.bcpp_survey.models import Survey

from ..search import PlotSearchByWord, PlotSearchByGps

site_mappers.autodiscover()


class SectionPlotView(BaseSectionView):
    section_name = 'plot'
    section_display_name = 'Plots'
    #add_model = Plot
    section_display_index = 10
    section_template = 'section_bcpp_plot.html'
    search = [PlotSearchByWord, PlotSearchByGps]

    def contribute_to_context(self, context, request, *args, **kwargs):
        current_community = site_mappers.get_current_mapper().map_area
        context.update({
            'current_survey': Survey.objects.current_survey(),
            'current_community': self.get_current_community(),
            'mapper_name': current_community,
            'use_gps_to_target_verification': settings.VERIFY_GPS
            })
        return context

    def get_current_community(self):
        return site_mappers.get_current_mapper().map_area

site_sections.register(SectionPlotView)
