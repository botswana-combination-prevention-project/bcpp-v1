import re

from django.db.models import Q

from edc.dashboard.search.classes import BaseSearchByWord

from ..models import HouseholdMember
from ..choices import HOUSEHOLD_MEMBER_PARTICIPATION


class MemberSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = HouseholdMember
    order_by = ['-modified']
    template = 'section_member_include.html'

    @property
    def qset(self):
        qset = self.qset_for_registered_subject
        qset.add(Q(household_structure__household__household_identifier__icontains=self.search_value), Q.OR)
        return qset

    @property
    def qset_by_search_term_pattern(self):
        qset_filter = None
        if re.match('^[0-9]{6}-[0-9]{2}$', self.search_value):
            qset_filter = Q(household_structure__household__plot__plot_identifier=self.search_value)
        elif re.match('^[0-9]{7}-[0-9]{2}$', self.search_value):
            qset_filter = Q(household_structure__household__household_identifier=self.search_value)
        if qset_filter:
            return (qset_filter, None)
        return None

    @property
    def keyword_list(self):
        """Returns a list of search values to be used to query."""
        return [item[0] for item in HOUSEHOLD_MEMBER_PARTICIPATION]

    @property
    def display_keyword_list(self):
        return [item[1] for item in HOUSEHOLD_MEMBER_PARTICIPATION]
