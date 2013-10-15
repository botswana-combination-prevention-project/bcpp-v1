from django.conf import settings

from edc.dashboard.search.classes import BaseSearchByWord

from ..models import Plot


class PlotSearchByWord(BaseSearchByWord):

    name = 'plot_word'
    search_model = Plot
    order_by = 'plot_identifier'
    template = 'search_plot_result_include.html'

    def get_most_recent_query_options(self):
        return {'community': settings.CURRENT_COMMUNITY}
