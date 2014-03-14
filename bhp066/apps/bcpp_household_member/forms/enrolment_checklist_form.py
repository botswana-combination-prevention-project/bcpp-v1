from datetime import date
from dateutil.relativedelta import relativedelta

from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import EnrolmentChecklist


class EnrolmentChecklistForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('citizen') == 'Yes':
            if not cleaned_data.get('legal_marriage') == 'N/A':
                raise forms.ValidationError('Marital status is not applicable, Participant is a citizen.')
            if not cleaned_data.get('marriage_certificate') == 'N/A':
                raise forms.ValidationError('Marriage Certificate is not applicable, Participant is a citizen.')
        if cleaned_data.get('citizen') == 'No':
            if cleaned_data.get('legal_marriage') == 'N/A':
                raise forms.ValidationError('Participant is not a citizen, indicate if he/she is legally married to a Botswana citizen.')
            if cleaned_data.get('legal_marriage') == 'N/A':
                raise forms.ValidationError('Participant is not a citizen, indicate if he/she is legally married to a Botswana citizen.')
            if cleaned_data.get('legal_marriage') == 'Yes' and (cleaned_data.get('marriage_certificate') == 'N/A' or cleaned_data.get('marriage_certificate') == ''):
                raise forms.ValidationError('Participant is legally married to a Botswana citizen, please provide the marriage certificate as proof?')
            if cleaned_data.get('legal_marriage') == 'Yes' and cleaned_data.get('marriage_certificate') == 'Yes':
                raise forms.ValidationError('Participant is legally married to a Botswana citizen, please provide the marriage certificate number?')
        if cleaned_data.get('household_member') and cleaned_data.get('gender'):
            if not cleaned_data.get('gender') == cleaned_data.get('household_member').gender:
                raise forms.ValidationError('Gender does not match with household member ({0})'.format(cleaned_data.get('household_member').first_name))
        if cleaned_data.get('household_member') and cleaned_data.get('initials'):
            if not cleaned_data.get('initials') == cleaned_data.get('household_member').initials:
                raise forms.ValidationError('Initials do not match with household member ({0}). Expected {1}.'.format(cleaned_data.get('household_member').first_name, cleaned_data.get('household_member').initials))
        return cleaned_data

    class Meta:
        model = EnrolmentChecklist
