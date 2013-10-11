from datetime import date
from django import forms
from ..models import HeartAttack, Cancer, Tubercolosis, Sti
from .base_subject_model_form import BaseSubjectModelForm


class HeartAttackForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(HeartAttackForm, self).clean()
        # to ensure that heartattack diagnosis date is not greater than today
        if cleaned_data.get('date_heart_attack'):
            if cleaned_data.get('date_heart_attack') > date.today():
                raise forms.ValidationError('The heart attack diagnoses date cannot be greater than today\'s date. Please correct.')
        return cleaned_data

    class Meta:
        model = HeartAttack


class CancerForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(CancerForm, self).clean()
        # to ensure that cancer diagnosis date is not greater than today
        if cleaned_data.get('date_cancer'):
            if cleaned_data.get('date_cancer') > date.today():
                raise forms.ValidationError('The cancer diagnoses date date cannot be greater than today\'s date. Please correct.')
        return cleaned_data

    class Meta:
        model = Cancer


class TubercolosisForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(CancerForm, self).clean()
        # to ensure that ctb diagnosis date is not greater than today
        if cleaned_data.get('date_tb'):
            if cleaned_data.get('date_tb') > date.today():
                raise forms.ValidationError('The tubercolosis diagnoses date date cannot be greater than today\'s date. Please correct.')
        return cleaned_data

    class Meta:
        model = Tubercolosis


class StiForm (BaseSubjectModelForm):
    
    def clean(self):
        cleaned_data = super(CancerForm, self).clean()
        # to ensure that STI diagnosis date is not greater than today
        if cleaned_data.get('sti_date'):
            if cleaned_data.get('sti_date') > date.today():
                raise forms.ValidationError('The STI diagnoses date date cannot be greater than today\'s date. Please correct.')
        return cleaned_data

    class Meta:
        model = Sti
