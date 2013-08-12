from bhp_search.classes import BaseSearchByWord, site_search
from models import SubjectConsent


class SubjectSearchByWord(BaseSearchByWord):

    section_name = 'subject'
    search_model = SubjectConsent
    order_by = '-created'
    template = 'subjectconsent_include.html'

site_search.register(SubjectSearchByWord)
