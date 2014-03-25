from django import forms
from ..models import HivTestingHistory
from .base_subject_model_form import BaseSubjectModelForm


class HivTestingHistoryForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(HivTestingHistoryForm, self).clean()

        #validating no prior hiv testing
        self.validate_prior_hiv_testing('when_hiv_test', cleaned_data)
        self.validate_prior_hiv_testing('has_record', cleaned_data)
        self.validate_prior_hiv_testing('other_record', cleaned_data)

        if cleaned_data.get('has_tested') == 'No' and cleaned_data.get('verbal_hiv_result'):
            raise forms.ValidationError('If participant has NEVER tested, do not provide details about testing results')

        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('when_hiv_test'):
            raise forms.ValidationError('If participant has tested before, let us know the last time he/she tested.')

        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('has_record'):
            raise forms.ValidationError('If participant has tested, is a record available? Got None.')

        return cleaned_data

    def validate_prior_hiv_testing(self, field, cleaned_data):
        msg = 'If participant has NEVER tested, do not provide testing details'
        self.validate_dependent_fields('has_tested', field, cleaned_data, msg)

    def validate_dependent_fields(self, master_field, sub_field, cleaned_data, msg):
        if cleaned_data.get(master_field, None) == 'No' and cleaned_data.get(sub_field, None):
            raise forms.ValidationError(msg)

    class Meta:
        model = HivTestingHistory
