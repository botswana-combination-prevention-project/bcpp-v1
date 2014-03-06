from django import forms
# from django.conf import settings
from edc.base.form.forms import BaseModelForm
#from edc.map.classes import site_mappers
# from edc.map.exceptions import MapperError
from ..models import Household, HouseholdStructure
from apps.bcpp_household_member.models import HouseholdMember


class HouseholdForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        plot = cleaned_data.get('plot', None)
        members = None
        if HouseholdStructure.objects.filter(household=self):
                h_structure = HouseholdStructure.objects.get(household=self)
                if HouseholdMember.objects.filter(household_structure=h_structure):
                    members = HouseholdMember.objects.filter(household_structure=h_structure)
        if cleaned_data.get('allowed_to_enumerate') == 'Yes' and members:
            raise forms.ValidationError("Household has already been enumerated, instead update members statuses to refusals.")
        if plot:
            if plot.is_dispatched():
                raise forms.ValidationError("Plot is currently dispatched. Data may not be changed.")
        return cleaned_data

    class Meta:
        model = Household
