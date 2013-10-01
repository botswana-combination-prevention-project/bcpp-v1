from django import forms
from ..models import HtcRegistration
from base_htc_scheduled_model_form import BaseHtcScheduledModelForm


class HtcRegistrationForm(BaseHtcScheduledModelForm):

    def clean(self):
        cleaned_data = super(HtcRegistrationForm, self).clean()
        household_structure = cleaned_data.get('household_structure', None)
        if household_structure:
            if household_structure.is_dispatched_as_item():
                raise forms.ValidationError("Household is currently dispatched. Data may not be changed.")
        return cleaned_data

    class Meta:
        model = HtcRegistration
