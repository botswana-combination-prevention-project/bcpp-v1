from django.conf import settings

from edc.dashboard.section.classes import BaseSectionView, site_sections
from edc.map.classes import site_mappers

from apps.bcpp_survey.models import Survey

from ..forms import GpsSearchForm
from ..models import Plot
from ..search import PlotSearchByWord, PlotSearchByGps

site_mappers.autodiscover()


class SectionPlotView(BaseSectionView):
    section_name = 'plot'
    section_display_name = 'Plots'
    add_model = Plot
    section_display_index = 10
    section_template = 'section_bcpp_plot.html'
    search_cls = [PlotSearchByWord, PlotSearchByGps]

    def contribute_to_context(self, context, request, *args, **kwargs):
        current_community = settings.CURRENT_COMMUNITY
        context.update({
            'current_survey': Survey.objects.current_survey(),
            'current_community': self.get_current_community(),
            'mapper_name': current_community,
            'gps_search_form': GpsSearchForm(initial={'community': self.get_current_community(), 'radius': 100})})
        return context

    def get_current_community(self):
        return settings.CURRENT_COMMUNITY

    def get_mapper(self):
        return site_mappers.get(self.get_current_community())()

site_sections.register(SectionPlotView)
