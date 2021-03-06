from django import forms

from ..models import HouseholdAssessment


class HouseholdAssessmentForm(forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('potential_eligibles') == 'Yes' and cleaned_data.get('eligibles_last_seen_home') is None:
            raise forms.ValidationError('Question 2 must be answered when question 1 answer is Yes.')
        return cleaned_data

    class Meta:
        model = HouseholdAssessment
        fields = '__all__'
