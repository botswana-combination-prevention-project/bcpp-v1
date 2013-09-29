from edc_core.bhp_household_member.forms import BaseHouseholdMemberForm
from ..models import HouseholdMember


class HouseholdMemberForm(BaseHouseholdMemberForm):

    class Meta:
        model = HouseholdMember
