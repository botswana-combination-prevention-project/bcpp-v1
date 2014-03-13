from datetime import date
from dateutil.relativedelta import relativedelta

from django import forms

from edc.base.form.forms import BaseModelForm

from ..models import RBDEligibility


class RBDEligibilityForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('household_member') and cleaned_data.get('dob'):
            print (cleaned_data.get('household_member').age_in_years - (relativedelta(date.today(), cleaned_data.get('dob'))).years)
            if not ((cleaned_data.get('household_member').age_in_years - (relativedelta(date.today(), cleaned_data.get('dob'))).years) <= 1 and (cleaned_data.get('household_member').age_in_years - (relativedelta(date.today(), cleaned_data.get('dob'))).years) >= -1):
                raise forms.ValidationError("The age difference of the household member form and enrollment checklist should be plus or minus 1 year.")
        return cleaned_data

    class Meta:
        model = RBDEligibility
