from django import forms
from edc.core.bhp_base_form.forms import BaseModelForm
from ..models import HouseholdInfo


class HouseholdInfoForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        #validating if other, specify
        if cleaned_data.get('flooring_type') == 'OTHER' and not cleaned_data.get('flooring_type_other'):
            raise forms.ValidationError('If participant has a different flooring type from what is on the list, provide the flooring type')
        if cleaned_data.get('water_source') == 'OTHER' and not cleaned_data.get('water_source_other'):
            raise forms.ValidationError('If participant uses a different water source, specify it')
        if cleaned_data.get('energy_source') == 'OTHER' and not cleaned_data.get('energy_source_other'):
            raise forms.ValidationError('If a different energy source is used, specify it')
        cleaned_data = super(HouseholdInfoForm, self).clean()
        return cleaned_data

    class Meta:
        model = HouseholdInfo
