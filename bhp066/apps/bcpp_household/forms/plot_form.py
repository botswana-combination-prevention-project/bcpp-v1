from django import forms

from edc.base.form.forms import BaseModelForm
from ..models import Plot


class PlotForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if self.instance.id:
            self.instance.household_count = self.instance.create_or_delete_households(self.instance)
            if self.instance.household_count > 0:
                self.cleaned_data['status'] = 'occupied'

        if not cleaned_data.get('household_count') and cleaned_data.get('status') == 'occupied':
            raise forms.ValidationError('Invalid number of households for plot that is {0}. Got {1}.'.format(cleaned_data.get('status'), cleaned_data.get('household_count')))

        if (cleaned_data.get('household_count') == 0 and cleaned_data.get('status') == 'occupied') or (cleaned_data.get('household_count') and not cleaned_data.get('status') == 'occupied'):
            raise forms.ValidationError('Invalid number of households for plot that is {0}. Got {1}.'.format(cleaned_data.get('status'), cleaned_data.get('household_count')))

        if not cleaned_data.get('status') == 'occupied' and cleaned_data.get('eligible_members') > 0:
            raise forms.ValidationError('If the residence is not occupied, number of eligible members should be 0. Got {0}'.format(cleaned_data.get('eligible_members')))

        if cleaned_data.get('status') == 'occupied' and (not cleaned_data.get('time_of_week') or not cleaned_data.get('time_of_day')):
            raise forms.ValidationError('If the residence is occupied, provide the best time to visit (e.g time of week, time of day).')

        if not cleaned_data.get('status') == 'occupied' and (cleaned_data.get('time_of_week') or cleaned_data.get('time_of_day')):
            raise forms.ValidationError('If the residence is NOT occupied, do not provide the best time to visit (e.g time of week, time of day).')
        return cleaned_data

    class Meta:
        model = Plot
