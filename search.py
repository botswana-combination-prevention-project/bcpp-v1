from bhp_search.classes import BaseSearchByWord, site_search
from section import SectionHouseholdView, SectionPlotView
from models import Household, Plot # , HouseholdStructure, HouseholdStructureMember


class HouseholdSearchByWord(BaseSearchByWord):

    section = SectionHouseholdView
    search_model = Household
    order_by = 'household_identifier'
    template = 'search_result_include.html'
    
    
    
class PlotSearchByWord(BaseSearchByWord):

    section = SectionPlotView
    search_model = Plot  # , HouseholdStructure, HouseholdStructureMember)
    order_by = 'plot_identifier'
    template = 'search_plot_result_include.html'

site_search.register(HouseholdSearchByWord)
site_search.register(PlotSearchByWord)