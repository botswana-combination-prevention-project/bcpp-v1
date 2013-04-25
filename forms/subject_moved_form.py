from django import forms
from base_membership_form import BaseMembershipForm
from bcpp_subject.models import SubjectMoved


class SubjectMovedForm(BaseMembershipForm):

    class Meta:
        model = SubjectMoved
