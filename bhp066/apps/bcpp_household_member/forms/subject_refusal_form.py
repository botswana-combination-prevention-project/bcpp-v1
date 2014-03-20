from django import forms
from ..models import SubjectRefusal
from .base_membership_form import BaseMembershipForm


class SubjectRefusalForm(BaseMembershipForm):

    def clean(self):
        cleaned_data = super(SubjectRefusalForm, self).clean()
        household_member = cleaned_data.get('household_member', None)
        offered_htc = cleaned_data.get('participant_offered_htc')
        if offered_htc is None:
            raise forms.ValidationError('The answer to question 6, must be either \'Yes\' or \' No\''.format(offered_htc))
        if offered_htc:
            if cleaned_data.get('accepted_htc') is None:
                raise forms.ValidationError('If participant was offered HTC please answer if they accepted or not.')
        if not offered_htc:
            if cleaned_data.get('accepted_htc'):
                raise forms.ValidationError('If participant was not offered HTC, then they could not have accepted it.')
        return cleaned_data

    class Meta:
        model = SubjectRefusal
