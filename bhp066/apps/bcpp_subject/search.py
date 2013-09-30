from edc.dashboard.search.classes import BaseSearchByWord, site_search
from .models import SubjectConsent
from .section import SectionSubjectView


class SubjectSearchByWord(BaseSearchByWord):

    section = SectionSubjectView
    search_model = SubjectConsent
    order_by = '-created'
    template = 'subjectconsent_include.html'

site_search.register(SubjectSearchByWord)
