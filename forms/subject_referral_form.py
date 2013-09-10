from base_membership_form import BaseMembershipForm
from bcpp_subject.models import SubjectReferral


class SubjectReferralForm(BaseMembershipForm):

    class Meta:
        model = SubjectReferral
