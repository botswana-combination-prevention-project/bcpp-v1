from django.db.models import Q
from django.conf import settings

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
        qset.add(Q(first_name__icontains=self.search_value), Q.OR)
        qset.add(Q(household_structure__household__household_identifier__icontains=self.search_value), Q.OR)
        qset.add(Q(household_structure__household__plot__plot_identifier__icontains=self.search_value), Q.OR)
        return qset

    @property
    def keyword_list(self):
        """Returns a list of search values to be used to query."""
        return [item[0] for item in HOUSEHOLD_MEMBER_PARTICIPATION]

    @property
    def display_keyword_list(self):
        return [item[1] for item in HOUSEHOLD_MEMBER_PARTICIPATION]

    def filtered_default_values(self):
        return {'household_structure__household__plot__community': settings.CURRENT_COMMUNITY}
