from django import forms
from datetime import date

from ..models import HivTestReview

from .base_subject_model_form import BaseSubjectModelForm
from bhp066.apps.bcpp_subject.models.hiv_testing_history import HivTestingHistory


class HivTestReviewForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(HivTestReviewForm, self).clean()
        self.clean_recorded_hiv_result(cleaned_data)
        if cleaned_data.get('hiv_test_date'):
            if cleaned_data.get('hiv_test_date') == date.today():
                raise forms.ValidationError('The HIV test date cannot be equal to today\'s date. Please correct.')
        return cleaned_data
    
    def clean_recorded_hiv_result(self, cleaned_data):
        subject_visit = cleaned_data.get("subject_visit")
        try:
            hiv_testing_history = HivTestingHistory.objects.get(subject_visit=subject_visit)
            if not hiv_testing_history.verbal_hiv_result == cleaned_data.get("recorded_hiv_result"):
                raise forms.ValidationError('The hiv status does not match, the status on'
                                            'hiv testing history {}, and hiv test review {}'.format(hiv_testing_history.verbal_hiv_result,
                                                                                            cleaned_data.get("recorded_hiv_result")
                                                                                            ))
        except HivTestingHistory.DoesNotExist:
            raise forms.ValidationError(
                    ' HivTestingHistory does not exist, please fill hiv testing history.'
            )

    class Meta:
        model = HivTestReview
