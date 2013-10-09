from django import forms

from ..models import Demographics
from .base_subject_model_form import BaseSubjectModelForm


class DemographicsForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(DemographicsForm, self).clean()
        # validating unmarried
        if cleaned_data.get('marital_status', None) != 'Married' and cleaned_data.get('num_wives', None):
            raise forms.ValidationError('If participant is not married, do not give number of wives')
        if cleaned_data.get('marital_status', None) != 'Married' and cleaned_data.get('husband_wives', None):
            raise forms.ValidationError('If participant is not married, the number of wives is not required')
        
        return cleaned_data

    class Meta:
        model = Demographics
