from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import FutureHivTesting


class FutureHivTestingForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data

        # validating a need to specify the participant's preference
        if cleaned_data.get('hiv_test_time') == 'Yes, specify' and not cleaned_data.get('hiv_test_time_other'):
            raise forms.ValidationError('If participant prefers a different test date/time than what is indicated, indicate the preference.')

        if cleaned_data.get('hiv_test_week') == 'Yes, specify' and not cleaned_data.get('hiv_test_week_other'):
            raise forms.ValidationError('If participant has preference for testing on a particular day of the week, indicate the preference.')

        if cleaned_data.get('hiv_test_year') == 'Yes, specify' and not cleaned_data.get('hiv_test_year_other'):
            raise forms.ValidationError('If participant prefers time of the year than the options given, indicate the preference.')

        cleaned_data = super(FutureHivTestingForm, self).clean()

        return cleaned_data

    class Meta:
        model = FutureHivTesting
