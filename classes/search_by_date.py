from bhp_search.classes import BaseSearchByDate
from search_models import SearchModels


class SearchByDate(BaseSearchByDate):

    def __init__(self, **kwargs):
        super(SearchByDate, self).__init__(**kwargs)
        search_models = SearchModels()
        self.search_model.update(**search_models.search_models)


# from bhp_search.classes import BaseSearchByDate
# from bcpp_subject.models import SubjectConsent
# 
# 
# class SearchByDate(BaseSearchByDate):
# 
#     def __init__(self, **kwargs):
# 
#         super(SearchByDate, self).__init__(**kwargs)
#         self.search_model.update({'subjectconsent': SubjectConsent})
