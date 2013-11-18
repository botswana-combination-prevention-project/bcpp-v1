from ..models import SubjectRefusal
from bcpp_household_member.forms import BaseMembershipForm


class SubjectRefusalForm(BaseMembershipForm):

    class Meta:
        model = SubjectRefusal
