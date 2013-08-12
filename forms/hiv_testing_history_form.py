from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import HivTestingHistory


class HivTestingHistoryForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(HivTestingHistoryForm, self).clean()
        #validating prior hiv testing
        if cleaned_data.get('has_tested') == 'No' and cleaned_data.get('when_hiv_test') and cleaned_data.get('has_record') and cleaned_data.get('other_record'):
            raise forms.ValidationError('If participant has NEVER tested, do not provide testing details')
        if cleaned_data.get('has_tested') == 'No' and cleaned_data.get('verbal_hiv_result'):
            raise forms.ValidationError('If participant has NEVER tested, do not provide details about testing results')
        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('when_hiv_test'):
            raise forms.ValidationError('If participant has tested before, let us know the last time he/she tested.')
        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('has_record'):
            raise forms.ValidationError('If participant has tested before, we need to know if a record is available.')
        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('verbal_hiv_result'):
            raise forms.ValidationError('If participant has tested before, let us know the result of the last HIV test (record the verbal response from the participant).')
        if cleaned_data.get('has_record') == 'Yes' and not cleaned_data.get('other_record'):
            raise forms.ValidationError('If participant has a record of prior HIV testing, check whether participant has any other record available for review.')
        return cleaned_data

    class Meta:
        model = HivTestingHistory
