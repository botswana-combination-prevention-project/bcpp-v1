from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import MedicalDiagnoses


class MedicalDiagnosesForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        #heart_attack
        if cleaned_data.get('diagnoses')[0].name == 'Heart Disease or Stroke' and not cleaned_data.get('heart_attack_record'):
            raise forms.ValidationError('If participant has ever had a heart attack, is there a record available?')
        #cancer
        if cleaned_data.get('diagnoses')[0].name == 'Cancer' and not cleaned_data.get('cancer_record'):
            raise forms.ValidationError('If participant has ever been diagnosed with cancer, is there a record available?')
        #sti
        if cleaned_data.get('diagnoses')[0].name == 'STI (Sexually Transmitted Infection)' and not cleaned_data.get('sti_record'):
            raise forms.ValidationError('If participant has ever been diagnosed with an STI, is there a record available?')
        #TB
        if cleaned_data.get('diagnoses')[0].name == 'Tubercolosis' and not cleaned_data.get('tb_record'):
            raise forms.ValidationError('If participant has ever been diagnosed with TB, is there a record available?')
        #if none
#         if cleaned_data.get('diagnoses')[0].name == 'Not Applicable' and cleaned_data.get('heart_attack_record') and cleaned_data.get('cancer_record'):
#             raise forms.ValidationError('If participant has NEVER EVER been diagnosed with any of the diagnoses listed, do not provide other details.')

        return cleaned_data

    class Meta:
        model = MedicalDiagnoses
