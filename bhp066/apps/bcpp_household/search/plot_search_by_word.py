from edc.dashboard.search.classes import BaseSearchByWord, site_search
from ..section import SectionPlotView
from ..models import Plot


class PlotSearchByWord(BaseSearchByWord):

    section = SectionPlotView
    search_model = Plot
    order_by = 'plot_identifier'
    template = 'search_plot_result_include.html'

site_search.register(PlotSearchByWord)
