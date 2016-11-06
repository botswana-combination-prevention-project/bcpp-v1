from django import forms

from ..models import HouseholdWorkList


class HouseholdWorkListForm(forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = HouseholdWorkList
        fields = '__all__'
