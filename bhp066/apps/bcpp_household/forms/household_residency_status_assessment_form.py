from django import forms
# from django.conf import settings
from edc.base.form.forms import BaseModelForm

from ..models import HouseholdResidencyStatusAssessment


class HouseholdResidencyStatusAssessmentForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('residency') == 'No' and not cleaned_data.get('last_seen_home'):
            raise forms.ValidationError('Question 9 must be answer when question 1 answer is No.')
        if cleaned_data.get('residency') == 'Yes' and not cleaned_data.get('member_count'):
            raise forms.ValidationError('If the answer to question 1 is yes question 2 must be answered.')
        if cleaned_data.get('citizen') == 'Yes' and not cleaned_data.get('how_many'):
            raise forms.ValidationError('The answer to question 3 is required if the answer to question 3 is yes.')
        if cleaned_data.get('citizen') == 'No':
            raise forms.ValidationError('No need to fill the form if member are not citizens.')
        if cleaned_data.get('citizen') == 'Dont_know' and not cleaned_data.get('most_likely'):
            raise forms.ValidationError('If the answer to question 3 is Don\'t know question 8 must be answered.')
        if cleaned_data.get('possible_eligibles') == 'Yes' and not cleaned_data.get('how_many_members'):
            raise forms.ValidationError('The number of members aged 16-64 is required on question 6.')
        if cleaned_data.get('possible_eligibles') == 'No':
            raise forms.ValidationError('Can not continue because there are no possible eligibles.')
        if cleaned_data.get('original_community') == 'Yes'and not cleaned_data.get('last_seen_home'):
            raise forms.ValidationError('The answer to question 9 is required if you say yes to question 7.')
        if cleaned_data.get('original_community') == 'Dont_know'and not cleaned_data.get('last_seen_home'):
            raise forms.ValidationError('The answer to question 9 is required if you say Don\'t know to question 7.')
        if cleaned_data.get('original_community') == 'No' and not cleaned_data.get('original_community_other'):
            raise forms.ValidationError('The answer to question 8 is required if you say No to question 7.')

        return cleaned_data

    class Meta:
        model = HouseholdResidencyStatusAssessment
