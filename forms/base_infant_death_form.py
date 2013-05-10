from django import forms
from bhp_base_form.forms import BaseModelForm


class BaseInfantDeathForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        #2
        if 'other' in cleaned_data['death_cause_info'].name.lower() and not cleaned_data['death_cause_other']:
            raise forms.ValidationError('You wrote \'other\' for the source of information for the cause of death category. Please specify.')
        # 4
        if 'other' in cleaned_data['death_cause_category'].name.lower() and not cleaned_data['death_cause_other']:
            raise forms.ValidationError('You wrote \'other\' for the cause of death category. Please specify.')
        # 6
        if cleaned_data['participant_hospitalized'].lower() == 'yes' and (not cleaned_data['death_reason_hospitalized'] or cleaned_data['days_hospitalized'] == 0):
            raise forms.ValidationError('You wrote that the particpant was hospitalized. Please provide a reason and for how many days')
        if cleaned_data['participant_hospitalized'].lower() == 'no' and (cleaned_data['death_reason_hospitalized'] or cleaned_data['days_hospitalized'] != 0):
            raise forms.ValidationError('You wrote that the particpant was NOT hospitalized but have provided a reason and for how many days. Please correct.')
        return cleaned_data
