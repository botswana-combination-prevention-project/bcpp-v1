from django import forms
from ..models import ClinicMain
from .base_clinic_model_form import BaseClinicModelForm


class ClinicMainForm (BaseClinicModelForm):

    def clean(self):

        cleaned_data = super(ClinicMainForm, self).clean()

        #if on ARV, CD4?
        if cleaned_data.get('on_arv', None) == 'Yes' and not cleaned_data.get('cd4_count'):
            raise forms.ValidationError('If participant is on ARV, what is the last known CD4 count?')

        #NO
        if (cleaned_data.get('on_arv', None) == 'No' or  cleaned_data.get('know_hiv_status', None) == 'DWTA') and cleaned_data.get('cd4_count'):
            raise forms.ValidationError('If participant is not on treatment, do not provide any other details')

        return cleaned_data

    class Meta:
        model = ClinicMain
