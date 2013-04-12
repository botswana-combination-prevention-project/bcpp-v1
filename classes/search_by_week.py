from bhp_search.classes import BaseSearchByWeek
from bcpp_subject.models import SubjectConsent


class SearchByWeek(BaseSearchByWeek):

    def __init__(self, **kwargs):

        super(SearchByWeek, self).__init__(**kwargs)
        self.search_model.update({'subjectconsent': SubjectConsent})
