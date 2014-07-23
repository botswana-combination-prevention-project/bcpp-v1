from django import forms

from ..models import Participation
from .base_subject_model_form import BaseSubjectModelForm


class ParticipationForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = super(ParticipationForm, self).clean()
        if cleaned_data.get('full').lower() == 'no' and cleaned_data.get('participation_type').lower() == 'not applicable':
            raise forms.ValidationError('If partial participation is chosen, you cannot choose \'Not Applicable\' in type of participation.')
        if cleaned_data.get('full').lower() == 'yes' and cleaned_data.get('participation_type').lower() != 'not applicable':
            raise forms.ValidationError('If full participation is chosen, you should choose \'Not Applicable\' in type of participation.')

        return cleaned_data

    class Meta:
        model = Participation
