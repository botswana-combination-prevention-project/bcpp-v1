import re

from django.db.models import Q

from edc.dashboard.search.classes import BaseSearchByWord

from ..models import HouseholdMember
from ..choices import HOUSEHOLD_MEMBER_ACTION


class MemberSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = HouseholdMember
    order_by = '-modified'
    template = 'section_member_include.html'

    def get_qset_by_search_term_pattern(self):
        qset_filter = Q()
        qset_exclude = Q()
        if re.match('^[0-9]{6}-[0-9]{2}$', self.get_search_term()):
            qset_filter = Q(household_structure__household__plot__plot_identifier=self.get_search_term())
        elif re.match('^[0-9]{7}-[0-9]{2}$', self.get_search_term()):
            qset_filter = Q(household_structure__household__household_identifier=self.get_search_term())
        if qset_filter:
            return qset_filter, qset_exclude
        return None

    def get_filter_keyword_list(self):
        return [item[1] for item in HOUSEHOLD_MEMBER_ACTION]

    def get_filter_keyword_url_list(self):
        pass

    def get_qset_by_filter_keyword(self):
        """Returns a qset based on matching keyword.

        If you predefine keywords, the search term will be intercepted and used to select a query instead."""
        qset_filter = Q()
        qset_exclude = Q()
        if self.get_search_term().lower() in [item[1].lower() for item in HOUSEHOLD_MEMBER_ACTION] + ['-{0}'.format(item[1].lower()) for item in HOUSEHOLD_MEMBER_ACTION]:
            if self.get_search_term()[0] == '-':
                search_term = [item[0] for item in HOUSEHOLD_MEMBER_ACTION if item == self.get_search_term()[1:]][0]
                qset_exclude = Q(member_status=search_term)
            else:
                search_term = [item[0] for item in HOUSEHOLD_MEMBER_ACTION if item[1].lower() == self.get_search_term().lower()][0]
                qset_filter = Q(member_status=search_term)
        if qset_filter or qset_exclude:
            return (qset_filter, qset_exclude)
        return None
