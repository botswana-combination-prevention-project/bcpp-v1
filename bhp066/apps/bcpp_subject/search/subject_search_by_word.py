from edc.dashboard.search.classes import BaseSearchByWord

from ..models import SubjectConsent


class SubjectSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = SubjectConsent
    order_by = '-created'
    template = 'subjectconsent_include.html'
