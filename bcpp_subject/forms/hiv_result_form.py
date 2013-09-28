from django import forms
from bcpp_subject.models import HivResult
from base_subject_model_form import BaseSubjectModelForm


class HivResultForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(HivResultForm, self).clean()
        # validating when testing declined
        if cleaned_data.get('hiv_result') == 'Declined' and not cleaned_data.get('why_not_tested'):
            raise forms.ValidationError('If participant has declined testing, provide reason participant declined testing')
        return cleaned_data

    class Meta:
        model = HivResult
