from django import forms

from ..models import Participation
from .base_subject_model_form import BaseSubjectModelForm


class ParticipationForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = super(ParticipationForm, self).clean()
        if cleaned_data.get('full').lower() == 'no' and not cleaned_data.get('description'):
            raise forms.ValidationError('If partial participation is chosen, you need to fill in the description field.')
        if cleaned_data.get('full').lower() == 'yes' and cleaned_data.get('description'):
            raise forms.ValidationError('If full participation is chosen, do not fill anything in the description field.')

        return cleaned_data

    class Meta:
        model = Participation
