from django import forms

from edc.constants import NOT_APPLICABLE

from apps.bcpp_survey.models import Survey

from ..models import HivTestingHistory

from .base_subject_model_form import BaseSubjectModelForm


class HivTestingHistoryForm (BaseSubjectModelForm):

    def __init__(self, *args, **kwargs):
        super(HivTestingHistoryForm, self).__init__(*args, **kwargs)
        # customize for annual surveys
        if Survey.objects.current_survey().survey_slug != Survey.objects.first_survey.survey_slug:
            self.fields['has_tested'].label = (
                'Since we last visited you have you been tested for HIV?')

    def clean(self):

        cleaned_data = super(HivTestingHistoryForm, self).clean()

        # validating no prior hiv testing
        self.validate_prior_hiv_testing('when_hiv_test', cleaned_data)
        self.validate_prior_hiv_testing('has_record', cleaned_data)
        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('when_hiv_test'):
            raise forms.ValidationError('If participant has tested before, let us know the last time he/she tested.')

        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('has_record'):
            raise forms.ValidationError('If participant has tested, is a record is available? Got None.')
        if (cleaned_data.get('has_tested') != 'Yes' and
            ((cleaned_data.get('has_record') is not None) or (cleaned_data.get('when_hiv_test') is not None) or
             (cleaned_data.get('verbal_hiv_result') is not None) or
             (cleaned_data.get('other_record') != NOT_APPLICABLE))):
            raise forms.ValidationError(
                'If participant has never tested, all questions should be answered None/Not Applicable.')
        if cleaned_data.get('verbal_hiv_result') != 'POS' and cleaned_data.get('other_record') != NOT_APPLICABLE:
            raise forms.ValidationError(
                'If participant is NOT POS, then any other documentation of HIV + should be Not Applicable.')
        if cleaned_data.get('verbal_hiv_result') == 'POS' and cleaned_data.get('other_record') == NOT_APPLICABLE:
            raise forms.ValidationError(
                'If participant is POS, then any other documentation of HIV + should be either \'Yes\' or \'No\'.')
        return cleaned_data

    def validate_prior_hiv_testing(self, field, cleaned_data):
        msg = 'If participant has NEVER tested, do not provide testing details'
        self.validate_dependent_fields('has_tested', field, cleaned_data, msg)

    def validate_dependent_fields(self, master_field, sub_field, cleaned_data, msg):
        if cleaned_data.get(master_field, None) == 'No' and cleaned_data.get(sub_field, None):
            raise forms.ValidationError(msg)

    class Meta:
        model = HivTestingHistory
