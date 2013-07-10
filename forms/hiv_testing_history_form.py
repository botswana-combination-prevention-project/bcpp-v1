from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import HivTestingHistory


#HivTestingHistory
class HivTestingHistoryForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating prior hiv testing
        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('when_hiv_test'):
            raise forms.ValidationError('If participant has tested before, let us know the last time he/she tested.')
        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('has_record'):
            raise forms.ValidationError('If participant has tested before, we need to know if a record is available.')
        if cleaned_data.get('has_record') == 'No' and not cleaned_data.get('verbal_hiv_result'):
            raise forms.ValidationError('If participant has tested before, let us know the result of the last HIV test.')
        cleaned_data = super(HivTestingHistoryForm, self).clean()
        return cleaned_data


    class Meta:
        model = HivTestingHistory
