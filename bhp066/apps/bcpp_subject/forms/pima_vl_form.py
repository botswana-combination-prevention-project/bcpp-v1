from django import forms

from ..models import PimaVl
from .base_subject_model_form import BaseSubjectModelForm
from edc_quota.override import Override


class PimaVlForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(PimaVlForm, self).clean()
        if cleaned_data.get('poc_vl_today') == 'No' and not cleaned_data.get('poc_vl_today'):
            raise forms.ValidationError('If POC VL NOT done today, please explain why not?')

        #If no PIMA CD4 performed, do not provide any CD4 related information
        if cleaned_data.get('poc_vl_today') == 'No' and cleaned_data.get('pima_id'):
            raise forms.ValidationError('Do not provide the PIMA machine id if the POC CD4 was not performed')
        if cleaned_data.get('poc_vl_today') == 'No' and cleaned_data.get('cd4_value'):
            raise forms.ValidationError('POC VL was not performed, do not provide the CD4 value')

        # If PIMA CD4 performed, provide details
        if cleaned_data.get('poc_vl_today') == 'Yes' and not cleaned_data.get('pima_id'):
            raise forms.ValidationError('If POC VL done today, please provide machine id?')
        if cleaned_data.get('poc_vl_today') == 'Yes' and not cleaned_data.get('cd4_value'):
            raise forms.ValidationError('If POC VL done today, what is the CD4 value?')
        if cleaned_data.get('poc_vl_today') == 'Yes' and not cleaned_data.get('cd4_datetime'):
            raise forms.ValidationError('If POC VL done today, what is the CD4 test datetime?')
        if cleaned_data.get('poc_vl_today') == 'Yes':
            if not (cleaned_data.get('time_of_test')  or cleaned_data.get('time_of_result')):
                raise forms.ValidationError('Time of test and time of result should be provided.')

        return cleaned_data

    class Meta:
        model = PimaVl
