from bcpp_subject.models import SubjectRefusal
from base_membership_form import BaseMembershipForm


class SubjectRefusalForm(BaseMembershipForm):

    class Meta:
        model = SubjectRefusal
