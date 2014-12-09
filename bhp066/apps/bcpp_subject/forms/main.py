from django import forms
from ..models import QualityOfLife, OutpatientCare, HivHealthCareCosts, SubstanceUse

from .base_subject_model_form import BaseSubjectModelForm


class QualityOfLifeForm (BaseSubjectModelForm):

    class Meta:
        model = QualityOfLife


class OutpatientCareForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(OutpatientCareForm, self).clean()

        if cleaned_data.get('govt_health_care') == 'Yes' and not cleaned_data.get('care_visits'):
            raise forms.ValidationError('If participant seeked care from Govt, how many outpatient '
                                        'visits were there?')

        if cleaned_data.get('govt_health_care') == 'Yes' and cleaned_data.get('facility_visited') == 'No visit in past 3 months':
            raise forms.ValidationError('If participant seeked care from Govt, answer about '
                                        'facility CANNOT be NO VISIT?')

        if cleaned_data.get('govt_health_care') == 'Yes' and not cleaned_data.get('care_reason'):
            raise forms.ValidationError('If participant seeked care from Govt, what was the '
                                        'primary reason for seeking care?')
        if cleaned_data.get('govt_health_care') == 'Yes' and cleaned_data.get('care_reason') == 'None':
            raise forms.ValidationError('If participant has seeked care, reason for receiving '
                                        'CANNOT be NONE?')
        if cleaned_data.get('govt_health_care') == 'Yes' and not cleaned_data.get('outpatient_expense'):
            raise forms.ValidationError('If participant seeked care from Govt, how much did he/she '
                                        'have to pay the health care provider?')
        if cleaned_data.get('govt_health_care') == 'Yes' and not cleaned_data.get('travel_time'):
            raise forms.ValidationError('how long did it take you to get to the clinic/hospital?')
        if cleaned_data.get('govt_health_care') == 'Yes' and cleaned_data.get('waiting_hours') == 'None':
            raise forms.ValidationError('If participant has seeked care, waiting hours to be '
                                        'seen cannot be None')
        return cleaned_data

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

        if cleaned_data.get('hiv_medical_care') == 'Yes' and cleaned_data.get('place_care_received') == 'None':
            raise forms.ValidationError('If participant has received HIV medical care, '
                                        'place where medical care received CANNOT be NONE? ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and not cleaned_data.get('care_regularity'):
            raise forms.ValidationError('If participant has received HIV medical care, how '
                                        'often was the care received? ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and not cleaned_data.get('doctor_visits'):
            raise forms.ValidationError('If participant has received HIV medical care, how '
                                        'often where you taken to see a doctor? ')

        if cleaned_data.get('hiv_medical_care') == 'No' and cleaned_data.get('place_care_received') != 'None':
            raise forms.ValidationError('If participant DID NOT received HIV medical care, then'
                                        'place care received should be NONE? ')

        return cleaned_data

    class Meta:
        model = HivHealthCareCosts


class SubstanceUseForm (BaseSubjectModelForm):

    class Meta:
        model = SubstanceUse
