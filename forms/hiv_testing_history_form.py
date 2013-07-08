from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import HivTestingHistory


#HivTestingHistory
class HivTestingHistoryForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #validating when testing declined
        if cleaned_data.get('hiv_result') == 'Declined' and not cleaned_data.get('why_not_tested'):
            raise forms.ValidationError('If participant has declined testing, provide reason participant declined testing (2)')
        #validating prior hiv testing
        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('when_hiv_test'):
            raise forms.ValidationError('If participant has tested before, let us know the last time he/she tested (20).')
        if cleaned_data.get('has_tested') == 'Yes' and not cleaned_data.get('verbal_hiv_result'):
            raise forms.ValidationError('If participant has tested before, provide what the result was (21).')
        cleaned_data = super(HivTestingHistoryForm, self).clean()
        return cleaned_data


    class Meta:
        model = HivTestingHistory
