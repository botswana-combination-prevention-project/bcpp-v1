from ..forms import GpsSearchForm
from ..models import Plot
from .base_search_by_gps import BaseSearchByGps


class PlotSearchByGps(BaseSearchByGps):

    name = 'gps'
    search_model = Plot
#     search_model_attrname = 'plot_identifier'
    order_by = 'plot_identifier'
    template = 'search_plot_result_include.html'
    search_form = GpsSearchForm
