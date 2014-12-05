from django import forms

from ..models import ResourceUtilization

from .base_subject_model_form import BaseSubjectModelForm


class ResourceUtilizationForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(ResourceUtilizationForm, self).clean()

        if cleaned_data.get('out_patient') == 'Yes' and not cleaned_data.get('hospitalized'):
            raise forms.ValidationError(
                'If participant sought medical care in the past 3months, how many times was he/she admitted?')

        if cleaned_data.get('out_patient') == 'Yes' and not cleaned_data.get('money_spent'):
            raise forms.ValidationError('How much money was spent?')

        if cleaned_data.get('out_patient') == 'Yes' and not cleaned_data.get('medical_cover'):
            raise forms.ValidationError('Did anyone else cover the costs?')

        return cleaned_data

    class Meta:
        model = ResourceUtilization
