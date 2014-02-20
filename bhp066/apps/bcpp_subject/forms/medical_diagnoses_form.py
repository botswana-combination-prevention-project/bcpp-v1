from django import forms
from ..models import MedicalDiagnoses
from .base_subject_model_form import BaseSubjectModelForm


class MedicalDiagnosesForm (BaseSubjectModelForm):
    def clean(self):
        cleaned_data = super(MedicalDiagnosesForm, self).clean()
        diagnoses_list = []
        for diagnoses in cleaned_data.get('diagnoses'):
            diagnoses_list.append(diagnoses.name)
        #heart_attack
        if 'Heart Disease or Stroke' in diagnoses_list and not cleaned_data.get('heart_attack_record'):
            raise forms.ValidationError('If participant has ever had a heart attack, is there a record available?')
        #cancer
        if 'Cancer' in diagnoses_list and not cleaned_data.get('cancer_record'):
            raise forms.ValidationError('If participant has ever been diagnosed with cancer, is there a record available?')
        #TB
        if 'Tubercolosis' in diagnoses_list and not cleaned_data.get('tb_record'):
            raise forms.ValidationError('If participant has ever been diagnosed with TB, is there a record available?')
        if 'None' in diagnoses_list and len(cleaned_data.get('diagnoses')) > 1:
            raise forms.ValidationError('The diagnosis can not be None and other diagonosis at the same time.')

        return cleaned_data

    class Meta:
        model = MedicalDiagnoses
