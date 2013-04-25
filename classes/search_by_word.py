from bhp_search.classes import BaseSearchByWord


class SearchByWord(BaseSearchByWord):

    def get_search_prep_models(self, **kwargs):
        return {'householdstructuremember': ('bcpp_household', 'householdstructuremember'),
                'householdstructure': ('bcpp_household', 'householdstructure'),
                'household': ('bcpp_household', 'household'),
                'subjectconsent': ('bcpp_subject', 'subjectconsent'),
                }



# from bhp_search.classes.base_search_by_word import BaseSearchByWord
# 
# 
# class SearchByWord(BaseSearchByWord):
# 
#     def get_search_prep_models(self):
# 
#         return {'subjectconsent': ('bcpp_subject', 'subjectconsent')}
