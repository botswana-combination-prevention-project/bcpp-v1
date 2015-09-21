from django import forms
from datetime import date

from ..models import HivTestReview

from .base_subject_model_form import BaseSubjectModelForm


class HivTestReviewForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(HivTestReviewForm, self).clean()
        if cleaned_data.get('hiv_test_date'):
            if cleaned_data.get('hiv_test_date') == date.today():
                raise forms.ValidationError('The HIV test date cannot be equal to today\'s date. Please correct.')
        return cleaned_data

    class Meta:
        model = HivTestReview
