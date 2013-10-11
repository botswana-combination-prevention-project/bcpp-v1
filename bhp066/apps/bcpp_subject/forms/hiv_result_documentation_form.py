from datetime import date
from django import forms
from ..models import HivResultDocumentation
from .base_subject_model_form import BaseSubjectModelForm


class HivResultDocumentationForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(HivResultDocumentationForm, self).clean()
        # to ensure that HIV test date is not equal nor greater than today
        if cleaned_data.get('result_date'):
            if cleaned_data.get('result_date') >= date.today():
                raise forms.ValidationError('The last recorded HIV test date cannot be greater or equal to today\'s date. Please correct.')
        return cleaned_data

    class Meta:
        model = HivResultDocumentation