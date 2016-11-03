from django import forms
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm
from ..models import Cd4Test


class Cd4TestForm (BaseHtcScheduledModelForm):

    def clean(self):
        cleaned_data = super(Cd4TestForm, self).clean()
        cd4_result = cleaned_data("cd4_result")
        referral_clinic = cleaned_data("referral_clinic")
        appointment_date = cleaned_data("appointment_date")
        if cd4_result is None or referral_clinic is None or appointment_date is None:
            raise forms.ValidationError("Please fill in all the fields below")
        return cleaned_data

    class Meta:
        model = Cd4Test
