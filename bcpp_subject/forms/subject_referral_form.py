from ..models import SubjectReferral
from .base_membership_form import BaseMembershipForm


class SubjectReferralForm(BaseMembershipForm):

    class Meta:
        model = SubjectReferral
