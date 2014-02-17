from django import forms
from ..models import SubjectRefusal
from .base_membership_form import BaseMembershipForm


class SubjectRefusalForm(BaseMembershipForm):

    def clean(self):
        cleaned_data = super(SubjectRefusalForm, self).clean()
        offered_htc = cleaned_data.get('participant_offered_htc')
        if offered_htc is None:
            raise forms.ValidationError('The answer to question 6, must be either \'Yes\' or \' No\''.format(offered_htc))
        return cleaned_data

    class Meta:
        model = SubjectRefusal
