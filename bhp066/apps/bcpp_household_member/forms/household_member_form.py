from base_household_member_form import BaseHouseholdMemberForm
from ..models import HouseholdMember


class HouseholdMemberForm(BaseHouseholdMemberForm):

    class Meta:
        model = HouseholdMember
