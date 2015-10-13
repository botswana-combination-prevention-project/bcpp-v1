from django import forms

from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import PreOrder


class PreOrderForm (BaseModelForm):

    def clean(self):
        cleaned_data = super(PreOrderForm, self).clean()
        self._meta.model().aliquot_exists_or_raise(
            cleaned_data.get('aliquot_identifier'),
            cleaned_data.get('subject_visit'),
            exception_cls=forms.ValidationError)
        self._meta.model().aliquot_unused_or_raise(
            cleaned_data.get('aliquot_identifier'),
            exception_cls=forms.ValidationError)
        return cleaned_data

    class Meta:
        model = PreOrder
