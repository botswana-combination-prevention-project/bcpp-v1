from django import forms
from bhp_common.utils import check_initials_field
from bhp_household_member.forms import BaseHouseholdMemberForm
from bcpp_household_member.models import HouseholdMember


class HouseholdMemberForm(BaseHouseholdMemberForm):

    class Meta:
        model = HouseholdMember
