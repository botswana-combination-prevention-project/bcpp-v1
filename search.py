from bhp_search.classes import BaseSearchByWord, search
from models import Household  # , HouseholdStructure, HouseholdStructureMember


class HouseholdSearchByWord(BaseSearchByWord):

    section_name = 'household'
    search_model = Household  # , HouseholdStructure, HouseholdStructureMember)

search.register(HouseholdSearchByWord)
