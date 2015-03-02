from django import forms
# from django.conf import settings
from edc.base.form.forms import BaseModelForm

from ..models import HouseholdAssessment


class HouseholdAssessmentForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('residency') == 'No' and not cleaned_data.get('last_seen_home'):
            raise forms.ValidationError('Question 6 must be answer when question 1 answer is No.')
        if cleaned_data.get('residency') == 'Yes' and not cleaned_data.get('member_count'):
            raise forms.ValidationError('If the answer to question 1 is yes question 2 must be answered.')
        if cleaned_data.get('member_count') and not cleaned_data.get('eligibles'):
            raise forms.ValidationError('If there are member please answer if eligible or not.')
        if cleaned_data.get('eligibles') == 'No' and not cleaned_data.get('ineligible_reason'):
            raise forms.ValidationError('Specify the reason why member are not eligible.')

        return cleaned_data

    class Meta:
        model = HouseholdAssessment
