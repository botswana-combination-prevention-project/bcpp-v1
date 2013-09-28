from edc_lib.bhp_search.classes import BaseSearchByWord, site_search
from .section import SectionHouseholdView, SectionPlotView
from .models import Household, Plot


class HouseholdSearchByWord(BaseSearchByWord):

    section = SectionHouseholdView
    search_model = Household
    order_by = 'household_identifier'
    template = 'search_result_include.html'

site_search.register(HouseholdSearchByWord)


class PlotSearchByWord(BaseSearchByWord):

    section = SectionPlotView
    search_model = Plot
    order_by = 'plot_identifier'
    template = 'search_plot_result_include.html'

site_search.register(PlotSearchByWord)
