from django import forms

from ..models import Household


class HouseholdForm(forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        plot = cleaned_data.get('plot', None)
        if plot:
            if plot.is_dispatched():
                raise forms.ValidationError("Plot is currently dispatched. Data may not be changed.")
        return cleaned_data

    class Meta:
        model = Household
        fields = '__all__'
