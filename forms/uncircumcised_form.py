from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import Uncircumcised


class UncircumcisedForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data
        # validate other
        if cleaned_data.get('circumcision_day') and not cleaned_data.get('circumcision_day_other'):
            raise forms.ValidationError('if \'YES\', specify the day preferred.')
        if cleaned_data.get('circumcision_week') and not cleaned_data.get('circumcision_week_other'):
            raise forms.ValidationError('if \'YES\', specify the week preferred.')
        if cleaned_data.get('circumcision_year') and not cleaned_data.get('circumcision_year_other'):
            raise forms.ValidationError('if \'YES\', specify the year preferred.')

        return cleaned_data

    class Meta:
        model = Uncircumcised
