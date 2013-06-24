from bhp_search.classes import BaseSearchByWord


class SearchByWord(BaseSearchByWord):

    def get_search_models_prep(self):
        return {'householdstructuremember': ('bcpp_household', 'householdstructuremember', 'household'),
                'householdstructure': ('bcpp_household', 'householdstructure', 'household'),
                'household': ('bcpp_household', 'household', 'household'),
                'subjectconsent': ('bcpp_subject', 'subjectconsent', 'subject'),
                }
