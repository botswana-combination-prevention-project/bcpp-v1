from django import forms
from ..models import HivResult
from .base_subject_model_form import BaseSubjectModelForm


class HivResultForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(HivResultForm, self).clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = HivResult(**self.cleaned_data)
        # validating that hiv_result is not changed after HicEnrollment is filled
        instance.hic_enrollment_checks(forms.ValidationError)
        # validating when testing declined
        if cleaned_data.get('hiv_result', None) == 'Declined' and not cleaned_data.get('why_not_tested', None):
            raise forms.ValidationError('If participant has declined testing, provide reason participant declined testing')

        # validating when testing not performed
        if cleaned_data.get('hiv_result', None) == 'Not performed' and cleaned_data.get('why_not_tested', None):
            raise forms.ValidationError('If testing was not performed, DO NOT provide reason for declining')

        # testing declined but giving test date
        if ((cleaned_data.get('hiv_result', None) == 'Declined') or (cleaned_data.get('hiv_result', None) == 'Not performed')) and (cleaned_data.get('hiv_result_datetime', None)):
            raise forms.ValidationError('If testing was declined or not performed, DO NOT give date and time of testing')

        # testing done but giving reason why not done
        if ((cleaned_data.get('hiv_result', None) == 'POS') or (cleaned_data.get('hiv_result', None) == 'NEG') or (cleaned_data.get('hiv_result', None) == 'IND')) and (cleaned_data.get('why_not_tested', None)):
            raise forms.ValidationError('If testing is performed, DO NOT provide reason for declining test')
 
        # testing done but not providing date
        if ((cleaned_data.get('hiv_result', None) == 'POS') or (cleaned_data.get('hiv_result', None) == 'NEG') or (cleaned_data.get('hiv_result', None) == 'IND')) and not (cleaned_data.get('hiv_result_datetime', None)):
            raise forms.ValidationError('If test has been performed, what is the test result date time?')


        return cleaned_data


    class Meta:
        model = HivResult
