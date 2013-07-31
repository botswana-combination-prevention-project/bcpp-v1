from bhp_search.classes import BaseSearchByWord, site_search
from models import Household  # , HouseholdStructure, HouseholdStructureMember


class HouseholdSearchByWord(BaseSearchByWord):

    section_name = 'household'
    search_model = Household  # , HouseholdStructure, HouseholdStructureMember)
    order_by = 'household_identifier'
    template = 'search_result_include.html'
site_search.register(HouseholdSearchByWord)
