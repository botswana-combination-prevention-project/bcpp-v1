from edc.dashboard.search.classes import BaseSearchByWord, site_search
from ..section import SectionHouseholdView
from ..models import Household


class HouseholdSearchByWord(BaseSearchByWord):

    section = SectionHouseholdView
    search_model = Household
    order_by = 'household_identifier'
    template = 'search_household_result_include.html'

site_search.register(HouseholdSearchByWord)
