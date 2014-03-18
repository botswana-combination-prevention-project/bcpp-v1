from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import HouseholdHeadEligibility


class HouseholdHeadEligibilityForm(BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        if cleaned_data.get('aged_over_18', None).lower() == 'yes' and cleaned_data.get('household_member', None).age_in_years < 18:
            raise forms.ValidationError('This household member\'s is recorded to be less than 18. Its \'{0}\'. But in this form you say they are 18 or older. Please correct.'.format(cleaned_data.get('household_member', None).age_in_years))
        return super(HouseholdHeadEligibilityForm, self).clean()

    class Meta:
        model = HouseholdHeadEligibility
