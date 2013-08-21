from bhp_search.classes import BaseSearchByWord, site_search
from models import HtcRegistration


class HtcSubjectSearchByWord(BaseSearchByWord):

    section_name = 'htc_subject'
    search_model = HtcRegistration
    order_by = '-created'
    template = 'htcregistration_include.html'

site_search.register(HtcSubjectSearchByWord)
