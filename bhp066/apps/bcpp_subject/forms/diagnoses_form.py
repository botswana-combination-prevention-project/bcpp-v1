from datetime import date
from django import forms
from ..models import HeartAttack, Cancer, Tubercolosis, Sti
from .base_subject_model_form import BaseSubjectModelForm


class HeartAttackForm (BaseSubjectModelForm):

    class Meta:
        model = HeartAttack


class CancerForm (BaseSubjectModelForm):

    class Meta:
        model = Cancer


class TubercolosisForm (BaseSubjectModelForm):

    class Meta:
        model = Tubercolosis


class StiForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(StiForm, self).clean()
        # to ensure that STI diagnosis date is not greater than today
        if cleaned_data.get('sti_date'):
            if cleaned_data.get('sti_date') > date.today():
                raise forms.ValidationError('The STI diagnoses date date cannot be greater than today\'s date. Please correct.')
        return cleaned_data

    class Meta:
        model = Sti
