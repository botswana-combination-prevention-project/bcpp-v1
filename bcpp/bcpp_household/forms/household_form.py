from django import forms

from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import Household


class HouseholdForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        plot = cleaned_data.get('plot', None)
        if plot:
            if plot.is_dispatched():
                raise forms.ValidationError("Plot is currently dispatched. Data may not be changed.")
        return cleaned_data

    class Meta:
        model = Household
