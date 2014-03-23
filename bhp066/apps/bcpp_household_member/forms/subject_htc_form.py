from ..models import SubjectHtc

from .base_membership_form import BaseMembershipForm


class SubjectHtcForm(BaseMembershipForm):

    class Meta:
        model = SubjectHtc
