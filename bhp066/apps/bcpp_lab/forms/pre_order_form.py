from django import forms

from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import PreOrder


class PreOrderForm (BaseModelForm):

    def clean(self):
        cleaned_data = super(PreOrderForm, self).clean()
        if self.instance and cleaned_data.get('aliquot_identifier'):
            self.instance.aliquot_exists_or_raise(
                aliqout_identifier=cleaned_data.get('aliquot_identifier'),
                subject_visit=self.instance.subject_visit,
                exception_cls=forms.ValidationError)
            self.instance.aliquot_unused_or_raise(
                pk=self.instance.id,
                aliquot_identifier=cleaned_data.get('aliquot_identifier'),
                exception_cls=forms.ValidationError)
        return cleaned_data

    class Meta:
        model = PreOrder
