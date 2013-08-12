from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import HivResult


class HivResultForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        # validating when testing declined
        if cleaned_data.get('hiv_result') == 'Declined' and not cleaned_data.get('why_not_tested'):
            raise forms.ValidationError('If participant has declined testing, provide reason participant declined testing')

        cleaned_data = super(HivResultForm, self).clean()

        return cleaned_data

    class Meta:
        model = HivResult
