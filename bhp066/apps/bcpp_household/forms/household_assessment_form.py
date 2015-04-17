from django import forms
# from django.conf import settings
from edc.base.form.forms import BaseModelForm

from ..models import HouseholdAssessment


class HouseholdAssessmentForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = HouseholdAssessment
