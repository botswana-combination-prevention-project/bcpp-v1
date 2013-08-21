from bhp_search.classes import BaseSearchByWord, site_search
from models import Household
from section import SectionHouseholdView


class HouseholdSearchByWord(BaseSearchByWord):

    section = SectionHouseholdView
    search_model = Household
    order_by = 'household_identifier'
    template = 'search_result_include.html'
site_search.register(HouseholdSearchByWord)
