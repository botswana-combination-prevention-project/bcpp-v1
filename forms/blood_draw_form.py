from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import BloodDraw


class BloodDrawForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = BloodDraw
