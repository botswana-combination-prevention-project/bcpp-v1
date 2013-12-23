from django import forms
from ..models import MedicalDiagnoses
from .base_subject_model_form import BaseSubjectModelForm


class MedicalDiagnosesForm (BaseSubjectModelForm):
    def clean(self):
        cleaned_data = super(MedicalDiagnosesForm, self).clean()
        #heart_attack
        if cleaned_data.get('diagnoses')[0].name == 'Heart Disease or Stroke' and not cleaned_data.get('heart_attack_record'):
            raise forms.ValidationError('If participant has ever had a heart attack, is there a record available?')
        #cancer
        if cleaned_data.get('diagnoses')[0].name == 'Cancer' and not cleaned_data.get('cancer_record'):
            raise forms.ValidationError('If participant has ever been diagnosed with cancer, is there a record available?')
        #sti - this has changed. no longer triggers the sti form - leaving it incase we revert
#         if cleaned_data.get('diagnoses')[0].name == 'STI (Sexually Transmitted Infection)' and not cleaned_data.get('sti_record'):
#             raise forms.ValidationError('If participant has ever been diagnosed with an STI, is there a record available?')
        #TB
        if cleaned_data.get('diagnoses')[0].name == 'Tubercolosis' and not cleaned_data.get('tb_record'):
            raise forms.ValidationError('If participant has ever been diagnosed with TB, is there a record available?')
        #validating inavailablity of records
        if cleaned_data.get('heart_attack_record') == 'No' and not cleaned_data.get('heart_attack_comment'):
            raise forms.ValidationError('if \'NO heart attack record\', please provide the VERBAL response of the diagnosis and date of diagnosis from the participant.')
        if cleaned_data.get('cancer_record') == 'No' and not cleaned_data.get('cancer_record_comment'):
            raise forms.ValidationError('if \'NO cancer record\', please provide the VERBAL response of the diagnosis and date of diagnosis from the participant.')
        if cleaned_data.get('tb_record') == 'No' and not cleaned_data.get('tb_record_comment'):
            raise forms.ValidationError('if \'NO TB record\', please provide the VERBAL response of the diagnosis and date of diagnosis from the participant.')

        return cleaned_data

    class Meta:
        model = MedicalDiagnoses
