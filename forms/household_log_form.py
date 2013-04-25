from django import forms
from bcpp_household.models import HouseholdLog, HouseholdLogEntry


class HouseholdLogForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super(HouseholdLogForm, self).clean()

        return cleaned_data

    class Meta:
        model = HouseholdLog


class HouseholdLogEntryForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super(HouseholdLogEntryForm, self).clean()

        return cleaned_data

    class Meta:
        model = HouseholdLogEntry
