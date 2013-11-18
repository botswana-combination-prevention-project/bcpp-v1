from ..models import SubjectMoved
from bcpp_household_member.forms import BaseMembershipForm


class SubjectMovedForm(BaseMembershipForm):

    class Meta:
        model = SubjectMoved
