from django import forms
from ..models import QualityOfLife, OutpatientCare, HivHealthCareCosts, Grant, SubstanceUse

from .base_subject_model_form import BaseSubjectModelForm


class QualityOfLifeForm (BaseSubjectModelForm):

    class Meta:
        model = QualityOfLife


class OutpatientCareForm (BaseSubjectModelForm):

    class Meta:
        model = OutpatientCare


class HivHealthCareCostsForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(HivHealthCareCostsForm, self).clean()

        if cleaned_data.get('hiv_medical_care') == 'Yes' and cleaned_data.get('reason_no_care') != None:
            raise forms.ValidationError('If participant has received HIV medical care, reason '
                                        'for not receiving care should be None ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and not cleaned_data.get('place_care_received'):
            raise forms.ValidationError('If participant has received HIV medical care, '
                                        'where was it received? ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and not cleaned_data.get('care_regularity'):
            raise forms.ValidationError('If participant has received HIV medical care, how '
                                        'often was the care received? ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and not cleaned_data.get('doctor_visits'):
            raise forms.ValidationError('If participant has received HIV medical care, how '
                                        'often where you taken to see a doctor? ')
        return cleaned_data

    class Meta:
        model = HivHealthCareCosts


class GrantForm (BaseSubjectModelForm):

    class Meta:
        model = Grant


class SubstanceUseForm (BaseSubjectModelForm):

    class Meta:
        model = SubstanceUse
