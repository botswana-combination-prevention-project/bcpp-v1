from datetime import date
from django import forms
from ..models import HivTestReview
from .base_subject_model_form import BaseSubjectModelForm


class HivTestReviewForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(HivTestReviewForm, self).clean()
        # to ensure that HIV test date is not greater than today
        if cleaned_data.get('hiv_test_date'):
            if cleaned_data.get('hiv_test_date') > date.today():
                raise forms.ValidationError('The last recorded HIV test date cannot be greater than today\'s date. Please correct.')
        return cleaned_data

    class Meta:
        model = HivTestReview
