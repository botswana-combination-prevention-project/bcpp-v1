from django import forms
from bcpp_household.models import HouseholdDescription


class HouseholdDescriptionForm(forms.Form):

    class Meta:
        model = HouseholdDescription