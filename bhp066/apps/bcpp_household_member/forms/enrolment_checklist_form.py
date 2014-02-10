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
            if not cleaned_data.get('marriage_certificate_no') == '':
                raise forms.ValidationError('Marriage Certificate Number is not required, Participant is a citizen.')
        if cleaned_data.get('citizen') == 'No':
            if cleaned_data.get('legal_marriage') == 'N/A':
                raise forms.ValidationError('Participant is not a citizen, indicate if he/she is legally married to a Botswana citizen.')
            if cleaned_data.get('legal_marriage') == 'No':
                raise forms.ValidationError('Participant is not a citizen and not legally married to a Botswana citizen. Participant is not eligible')
            if cleaned_data.get('legal_marriage') == 'N/A':
                raise forms.ValidationError('Participant is not a citizen, indicate if he/she is legally married to a Botswana citizen.')
            if cleaned_data.get('legal_marriage') == 'Yes' and (cleaned_data.get('marriage_certificate') == 'N/A' or cleaned_data.get('marriage_certificate') == ''):
                raise forms.ValidationError('Participant is legally married to a Botswana citizen, please provide the marriage certificate as proof?')
            if cleaned_data.get('legal_marriage') == 'Yes' and cleaned_data.get('marriage_certificate') == 'No':
                raise forms.ValidationError('Participant says he/she is married to a Botswana citizen but cannot produce the certificate as proof. Participant is not eligible.')
            if cleaned_data.get('legal_marriage') == 'Yes' and cleaned_data.get('marriage_certificate') == 'Yes' and (cleaned_data.get('marriage_certificate_no') == ''):
                raise forms.ValidationError('Participant is legally married to a Botswana citizen, please provide the marriage certificate number?')
        if cleaned_data.get('household_member') and cleaned_data.get('gender'):
            if not cleaned_data.get('gender') == cleaned_data.get('household_member').gender:
                raise forms.ValidationError('Gender does not match with household member ({0})'.format(cleaned_data.get('household_member').first_name))
        if cleaned_data.get('household_member') and cleaned_data.get('initials'):
            if not cleaned_data.get('initials') == cleaned_data.get('household_member').initials:
                raise forms.ValidationError('Initials do not match with household member ({0}). Expected {1}.'.format(cleaned_data.get('household_member').first_name, cleaned_data.get('household_member').initials))
        if cleaned_data.get('household_member') and cleaned_data.get('dob'):
            print (cleaned_data.get('household_member').age_in_years - (relativedelta(date.today(), cleaned_data.get('dob'))).years)
            if not ((cleaned_data.get('household_member').age_in_years - (relativedelta(date.today(), cleaned_data.get('dob'))).years) <=1 and   (cleaned_data.get('household_member').age_in_years - (relativedelta(date.today(), cleaned_data.get('dob'))).years) >=-1):
                raise forms.ValidationError("The age difference of the household member form and enrollment checklist should be plus or minus 1 year.")
        return cleaned_data

    class Meta:
        model = EnrolmentChecklist
