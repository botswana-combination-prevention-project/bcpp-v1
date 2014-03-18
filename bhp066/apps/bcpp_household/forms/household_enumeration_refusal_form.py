from django import forms

from edc.base.form.forms import BaseModelForm

from ..models import HouseholdEnumerationRefusal


class HouseholdEnumerationRefusalForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('reason') == 'other':
            raise forms.ValidationError("If other for the question above please abswer question 3.")
        return cleaned_data

    class Meta:
        model = HouseholdEnumerationRefusal
