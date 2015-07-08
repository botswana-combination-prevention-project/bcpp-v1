from django import forms
from django.conf import settings

from ..models import PimaVl
from .base_subject_model_form import BaseSubjectModelForm

from apps.bcpp_tracking.classes import TrackerHelper


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

        tracker = TrackerHelper()
        if tracker.tracked_value.tracked_value >= tracker.tracked_value.value_limit:
            raise forms.ValidationError('The number of POC vl for {0} cannot be greater than {1} '.format(settings.PIMA_VL_TYPE, tracker.tracked_value.value_limit))

        return cleaned_data

    class Meta:
        model = PimaVl
