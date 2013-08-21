from django import forms
from base_htc_model_form import BaseHtcModelForm
from bcpp_htc.models import HivTestingHistory


class HivTestingHistoryForm (BaseHtcModelForm):
    
    def clean(self):
        cleaned_data = super(HivTestingHistoryForm, self).clean()
        # validating testing
        if cleaned_data.get('previous_testing') == 'Yes' and not cleaned_data.get('testing_place'):
            raise forms.ValidationError('If participant has previously tested for HIV, where did'
                                        ' the participant last undergo the testing?')
        if cleaned_data.get('previous_testing') == 'Yes' and not cleaned_data.get('hiv_record'):
            raise forms.ValidationError('If participant has previously tested for HIV, '
                                        'is a record of last HIV test available?')
        return cleaned_data

    class Meta:
        model = HivTestingHistory
