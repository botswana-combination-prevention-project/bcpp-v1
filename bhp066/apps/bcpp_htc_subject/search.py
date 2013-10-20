from edc.dashboard.search.classes import BaseSearchByWord
from .models import HtcRegistration
from .section import SectionHtcSubjectView


class HtcSubjectSearchByWord(BaseSearchByWord):

    section = SectionHtcSubjectView
    search_model = HtcRegistration
    order_by = '-created'
    template = 'htcregistration_include.html'
