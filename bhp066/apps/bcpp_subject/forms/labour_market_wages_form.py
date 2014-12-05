from django import forms
from ..models import LabourMarketWages
from .base_subject_model_form import BaseSubjectModelForm


class LabourMarketWagesForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(LabourMarketWagesForm, self).clean()
        grant = self.cleaned_data.get('grant')
        # if yes, answer next question
        if cleaned_data.get('govt_grant') == 'Yes':
            if not grant:
                raise forms.ValidationError('You are to answer questions about Grant')
        return cleaned_data

    class Meta:
        model = LabourMarketWages
