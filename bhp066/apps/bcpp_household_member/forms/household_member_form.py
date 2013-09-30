from edc.survey.household_member.forms import BaseHouseholdMemberForm
from ..models import HouseholdMember


class HouseholdMemberForm(BaseHouseholdMemberForm):

    class Meta:
        model = HouseholdMember
