from django import forms

from ..models import ClinicEligibility

from edc.base.form.forms import BaseModelForm


class ClinicEligibilityForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(ClinicEligibilityForm, self).clean()
        self.instance.match_consent_values(ClinicEligibility(**cleaned_data), forms.ValidationError)

        return cleaned_data

    class Meta:
        model = ClinicEligibility
