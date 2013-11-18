from django import forms
# from django.conf import settings
from edc.base.form.forms import BaseModelForm
# from edc.map.classes import site_mappers
# from edc.map.exceptions import MapperError
from ..models import Household


# def get_mapper():
#     mapper = site_mappers.get(settings.CURRENT_MAPPER)
#     if not mapper:
#         raise MapperError('Mapper not registered for community {0}.'.format(settings.CURRENT_MAPPER))
#     return mapper()


class HouseholdForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        plot = cleaned_data.get('plot', None)
        if plot:
            if plot.is_dispatched_as_item():
                raise forms.ValidationError("Plot is currently dispatched. Data may not be changed.")
        return cleaned_data

    class Meta:
        model = Household
