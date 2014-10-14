from django import forms

from ..models import ClinicQuestionnaire
from .base_clinic_model_form import BaseClinicModelForm


class ClinicQuestionnaireForm (BaseClinicModelForm):

    def clean(self):

        cleaned_data = super(ClinicQuestionnaireForm, self).clean()

        if cleaned_data.get('knows_last_cd4', None) == 'Yes' and not cleaned_data.get('cd4_count', None):
            raise forms.ValidationError('Participant answered that they know their last CD4 value, please provide this value.')

        if cleaned_data.get('knows_last_cd4', None) != 'Yes' and cleaned_data.get('cd4_count', None):
            raise forms.ValidationError('Participant answered \'{0}\' to knowledge of their CD4 result. Do not provide this value.'.format(cleaned_data.get('knows_last_cd4', None)))

        if cleaned_data.get('other_identifiers', None) != 'None' and not cleaned_data.get('htc_and_or_pims', None):
            raise forms.ValidationError('Participant reports to have either HTC, PIMS identifier or both. Please enter that identifier.')

        if cleaned_data.get('other_identifiers', None) == 'None' and cleaned_data.get('htc_and_or_pims', None):
            raise forms.ValidationError('Participant reports to NOT have either HTC, PIMS identifier or both. Please DO NOT enter any identifier.')

        return cleaned_data

    class Meta:
        model = ClinicQuestionnaire
