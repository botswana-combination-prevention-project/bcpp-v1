from django import forms
from ..models import HivResult
from .base_subject_model_form import BaseSubjectModelForm


class HivResultForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(HivResultForm, self).clean()
        
        # validating when testing declined
        if cleaned_data.get('hiv_result', None) == 'Declined' and not cleaned_data.get('why_not_tested', None):
            raise forms.ValidationError('If participant has declined testing, provide reason participant declined testing')
        
        #testing declined but giving test date
        if ((cleaned_data.get('hiv_result', None) == 'Declined' or 'Not performed') and cleaned_data.get('hiv_result_datetime', None)):
            raise forms.ValidationError('If testing was NOT done, DO NOT give date and time of testing')
        
        #testing done but giving reason why not done
        if ((cleaned_data.get('hiv_result', None) != 'Declined' or 'Not performed') and cleaned_data.get('why_not_tested', None)):
            raise forms.ValidationError('If testing is performed, DO NOT provide reason for declining test')
        
        #testing done but not providing date
        if ((cleaned_data.get('hiv_result', None) != 'Declined' or 'Not performed') and not cleaned_data.get('hiv_result_datetime', None)):
            raise forms.ValidationError('If test has been performed, what is the test result date time?')
        
        return cleaned_data

    class Meta:
        model = HivResult
