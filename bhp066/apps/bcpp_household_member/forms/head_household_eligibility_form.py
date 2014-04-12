from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import HouseholdHeadEligibility


class HouseholdHeadEligibilityForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(HouseholdHeadEligibilityForm, self).clean()
        if HouseholdHeadEligibility.objects.filter(household_structure=cleaned_data.get('household_structure'), aged_over_18='Yes', verbal_script='Yes').exists():
            raise forms.ValidationError('You have already entered an eligible head of household. DO NOT enter another one. Continue with Survey.')
        if cleaned_data.get('household_member', None) is None:
            raise forms.ValidationError('You have to select a household member in order to save.')
        self.instance.matches_household_member_values(cleaned_data.get('household_member'), forms.ValidationError)
        return cleaned_data

    class Meta:
        model = HouseholdHeadEligibility
