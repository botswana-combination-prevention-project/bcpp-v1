from datetime import date
from django import forms
from ..models import HivMedicalCare
from .base_subject_model_form import BaseSubjectModelForm


class HivMedicalCareForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(HivMedicalCareForm, self).clean()
        #What about those who actually only started receiving medical care today?
        if cleaned_data.get('first_hiv_care_pos'):
            if cleaned_data.get('first_hiv_care_pos') == date.today():
                raise forms.ValidationError('Date first received medical care cannot be equal to today. Please correct.')
        return cleaned_data

    class Meta:
        model = HivMedicalCare