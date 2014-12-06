from django import forms
from ..models import HospitalAdmission
from .base_subject_model_form import BaseSubjectModelForm


class HospitalAdmissionForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(HospitalAdmissionForm, self).clean()
        # if zero, don't answer next questions
        self.validate_cleaned_data('reason_hospitalized', cleaned_data)
        self.validate_cleaned_data('facility_hospitalized', cleaned_data)
        self.validate_cleaned_data('nights_hospitalized', cleaned_data)
        self.validate_cleaned_data('healthcare_expense', cleaned_data)
        self.validate_cleaned_data('travel_hours', cleaned_data)
        self.validate_cleaned_data('hospitalization_costs', cleaned_data)

        # if greater than zero
        if cleaned_data.get('admission_nights') > 0 and not cleaned_data.get('reason_hospitalized'):
            raise forms.ValidationError(
                'If admission nights is greater than zero, what was the reason for hospitalization?')
        if cleaned_data.get('admission_nights') > 0 and not cleaned_data.get('facility_hospitalized'):
            raise forms.ValidationError(
                'If admission nights is greater than zero, where was the participant hospitalized?')
        if cleaned_data.get('admission_nights') > 0 and not cleaned_data.get('nights_hospitalized'):
            raise forms.ValidationError(
                'For how many nights in total was the participant hospitalized?')
#         if cleaned_data.get('admission_nights') > 0 and not cleaned_data.get('healthcare_expense'):
#             raise forms.ValidationError(
#                 'How much was paid for the entire stay including medicines?')
        if cleaned_data.get('admission_nights') > 0 and not cleaned_data.get('travel_hours'):
            raise forms.ValidationError(
                'How many hours did it take you to get to the hospital?')
#         if cleaned_data.get('admission_nights') > 0 and not cleaned_data.get('hospitalization_costs'):
#             raise forms.ValidationError(
#                 'Did anyone else besides you cover the hospitalization costs?')

        def validate_greater_than_zero_admission_nights(self, field, cleaned_data):
            msg = 'DO NOT provide any hospital details IF hospitalization nights is NOT GREATER than ZERO'
            self.validate_dependent_fields('admission_nights', field, cleaned_data, msg)

        def validate_dependent_fields(self, master_field, sub_field, cleaned_data, msg):
            if cleaned_data.get(master_field, None) == 0 and cleaned_data.get(sub_field, None):
                raise forms.ValidationError(msg)

        return cleaned_data

    class Meta:
        model = HospitalAdmission
