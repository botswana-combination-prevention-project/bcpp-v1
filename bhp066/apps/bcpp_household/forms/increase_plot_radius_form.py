from django import forms

from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import IncreasePlotRadius


class IncreasePlotRadiusForm(BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('radius') < 25.0:
            raise forms.ValidationError('The value of the radius should be greater '
                                        'than 25.0 meters. Got {0}'.format(cleaned_data.get('radius')))
        if cleaned_data.get('radius') > 50:
            raise forms.ValidationError('The value of the radius should be less '
                                        'than 50. Got {0}'.format(cleaned_data.get('radius')))
        return cleaned_data

    class Meta:
        model = IncreasePlotRadius
