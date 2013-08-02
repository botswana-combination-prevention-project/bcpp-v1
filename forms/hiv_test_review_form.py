from datetime import date
from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import HivTestReview


class HivTestReviewForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        # to ensure that HIV test date is not greater than today
        if cleaned_data.get('hiv_test_date'):
            if cleaned_data.get('hiv_test_date') > date.today():
                raise forms.ValidationError('The last recorded HIV test date cannot be greater than today\'s date. Please correct.')

        return super(HivTestReviewForm, self).clean()

    class Meta:
        model = HivTestReview
