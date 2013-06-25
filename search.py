from bhp_search.classes import BaseSearchByWord, search
#from bccp_household.models import Household, HouseholdStructure, HouseholdStructureMember
from models import SubjectConsent


class SubjectSearchByWord(BaseSearchByWord):

    section_name = 'subject'
    search_model = SubjectConsent  # (SubjectConsent, Household, HouseholdStructure, HouseholdStructureMember)

search.register(SubjectSearchByWord)

# from bhp_search.classes import BaseSearchByWord, search
#
# class SearchByWord(BaseSearchByWord):
#
#     def get_search_models_prep(self):
#         return {'householdstructuremember': ('bcpp_household', 'householdstructuremember', 'household'),
#                 'householdstructure': ('bcpp_household', 'householdstructure', 'household'),
#                 'household': ('bcpp_household', 'household', 'household'),
#                 'subjectconsentyearzero': ('bcpp_subject', 'subjectconsentyearzero', 'subject'),
#                 }
#
#
# search.register(SearchByWord)
