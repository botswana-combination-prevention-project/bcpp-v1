from bhp_search.classes import BaseSearchByDate
from bcpp_subject.models import SubjectConsent


class SearchByDate(BaseSearchByDate):

    def __init__(self, **kwargs):

        super(SearchByDate, self).__init__(**kwargs)
        self.search_model.update({'subjectconsent': SubjectConsent})
