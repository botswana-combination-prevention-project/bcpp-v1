from django import forms
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm
from ..models import CircumcisionAppointment


class CircumcisionAppointmentForm (BaseHtcScheduledModelForm):

    def clean(self):
        cleaned_data = super(CircumcisionAppointmentForm, self).clean()
        circumcision_ap = cleaned_data.get("circumcision_ap")
        circumcision_ap_date = cleaned_data.get("circumcision_ap_date")

        if circumcision_ap == 'No'and circumcision_ap_date is not None:
            raise forms.ValidationError("No appointment was made.You cannot enter a date.Please correct.")

        if circumcision_ap == 'Yes'and circumcision_ap_date is None:
            raise forms.ValidationError("Please enter a date.")

        return cleaned_data

    class Meta:
        model = CircumcisionAppointment
