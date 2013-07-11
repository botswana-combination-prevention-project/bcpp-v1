from bhp_household_member.forms import BaseHouseholdMemberForm
from bcpp_household_member.models import HouseholdMember


class HouseholdMemberForm(BaseHouseholdMemberForm):

    class Meta:
        model = HouseholdMember
