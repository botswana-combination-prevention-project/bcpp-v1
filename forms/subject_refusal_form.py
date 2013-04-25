from base_membership_form import BaseMembershipForm
from bcpp_subject.models import SubjectRefusal


class SubjectRefusalForm(BaseMembershipForm):

    class Meta:
        model = SubjectRefusal
