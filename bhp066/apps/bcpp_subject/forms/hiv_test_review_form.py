from django import forms

from ..models import HivTestReview
from .base_subject_model_form import BaseSubjectModelForm


class HivTestReviewForm (BaseSubjectModelForm):

    def clean(self):
        self.instance.validate_participation_type(HivTestReview(**self.cleaned_data), exception_cls=forms.ValidationError)
        return super(HivTestReviewForm, self).clean()

    class Meta:
        model = HivTestReview
