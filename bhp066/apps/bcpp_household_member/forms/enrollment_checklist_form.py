from django import forms

from edc.base.form.forms import BaseModelForm

from ..models import EnrollmentChecklist


class EnrollmentChecklistForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(EnrollmentChecklistForm, self).clean()

        if not cleaned_data.get('household_member'):
            raise forms.ValidationError('Please select a household member.')

        if cleaned_data.get('household_member').is_consented:
            raise forms.ValidationError('Household member has consented. Enrollment Checklist may not be modified')

        self.instance.matches_household_member_values(EnrollmentChecklist(**cleaned_data), cleaned_data.get('household_member'), forms.ValidationError)

        if cleaned_data.get('citizen') == 'Yes':
            if not cleaned_data.get('legal_marriage') == 'N/A':
                raise forms.ValidationError('Marital status is not applicable, Participant is a citizen.')
            if not cleaned_data.get('marriage_certificate') == 'N/A':
                raise forms.ValidationError('Marriage Certificate is not applicable, Participant is a citizen.')

        if cleaned_data.get('citizen') == 'No':
            if cleaned_data.get('legal_marriage') == 'N/A':
                raise forms.ValidationError('Participant is not a citizen, indicate if he/she is legally married to a Botswana citizen.')
        if not cleaned_data.get('gender') == cleaned_data.get('household_member').gender:
            raise forms.ValidationError('Gender does not match with household member ({0})'.format(cleaned_data.get('household_member').first_name))
        if not cleaned_data.get('initials') == cleaned_data.get('household_member').initials:
            raise forms.ValidationError('Initials do not match with household member ({0}). Expected {1}.'.format(cleaned_data.get('household_member').first_name, cleaned_data.get('household_member').initials))

        if cleaned_data.get('is_minor') == 'Yes' and not cleaned_data.get('household_member').is_minor:
            raise forms.ValidationError('Is Subject a minor? Got {0} years from household member.'.format(cleaned_data.get('household_member').age_in_years))
        if cleaned_data.get('is_minor') == 'N/A' and cleaned_data.get('household_member').is_minor:
            raise forms.ValidationError('Is Subject a minor? Got {0} years from household member'.format(cleaned_data.get('household_member').age_in_years))

        return cleaned_data

    class Meta:
        model = EnrollmentChecklist
