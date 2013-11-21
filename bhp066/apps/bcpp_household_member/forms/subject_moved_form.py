from ..models import SubjectMoved
from .base_membership_form import BaseMembershipForm


class SubjectMovedForm(BaseMembershipForm):

    class Meta:
        model = SubjectMoved
