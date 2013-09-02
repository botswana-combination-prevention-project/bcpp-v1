from django import forms
from bhp_base_form.forms import BaseModelForm
from bcpp_subject_htc.models import HtcRegistration


class HtcRegistrationForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(HtcRegistrationForm, self).clean()
        household_structure = cleaned_data.get('household_structure', None)
        if household_structure:
            if household_structure.is_dispatched_as_item():
                raise forms.ValidationError("Household is currently dispatched. Data may not be changed.")
        return cleaned_data

    class Meta:
        model = HtcRegistration
