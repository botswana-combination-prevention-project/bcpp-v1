from django import forms

from edc.base.form.forms import BaseModelForm

from ..models import ClinicVlResult


class ClinicVlResultForm (BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('assay_date', None) <= cleaned_data.get('collection_datetime', None).date():
            raise forms.ValidationError('Assay date CANNOT be less than or equal to '
                                        'the date sample drawn. Please correct.')

        return cleaned_data

    class Meta:
        model = ClinicVlResult
