from edc_core.bhp_search.classes import BaseSearchByWord, site_search
from .models import HtcRegistration
from .section import SectionHtcSubjectView


class HtcSubjectSearchByWord(BaseSearchByWord):

    section = SectionHtcSubjectView
    search_model = HtcRegistration
    order_by = '-created'
    template = 'htcregistration_include.html'

#site_search.register(HtcSubjectSearchByWord)
