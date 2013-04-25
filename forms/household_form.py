from django import forms
from bcpp_household.models import Household


class HouseholdForm(forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        # check if supplied old identifier is already in sue
        old_household_identifier = cleaned_data.get('old_household_identifier', None)
        if old_household_identifier:
            if Household.objects.filter(household_identifier=old_household_identifier).exists():
                raise forms.ValidationError("{0} already exists".format(old_household_identifier))
        if not cleaned_data.get('gps_point_1') == '24':
            raise forms.ValidationError('GPS S must be 24. Got %s' % (cleaned_data.get('gps_point_1'),))
        if not cleaned_data.get('gps_point_2') == '26':
            raise forms.ValidationError('GPS E must be 26. Got %s' % (cleaned_data.get('gps_point_2'),))

        return cleaned_data

    class Meta:
        model = Household
