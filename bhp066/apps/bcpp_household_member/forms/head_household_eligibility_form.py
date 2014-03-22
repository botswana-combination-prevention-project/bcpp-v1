from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import HouseholdHeadEligibility


class HouseholdHeadEligibilityForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(HouseholdHeadEligibilityForm, self).clean()
        self.instance.matches_household_member_values(cleaned_data.get('household_member'), forms.ValidationError)
        return cleaned_data

    class Meta:
        model = HouseholdHeadEligibility
