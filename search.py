from bhp_search.classes import BaseSearchByWord, site_search
from models import Household  # , HouseholdStructure, HouseholdStructureMember


class HouseholdSearchByWord(BaseSearchByWord):

    section_name = 'household'
    search_model = Household  # , HouseholdStructure, HouseholdStructureMember)

site_search.register(HouseholdSearchByWord)
