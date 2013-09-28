from django import forms
from bcpp_subject.models import Pima
from base_subject_model_form import BaseSubjectModelForm


class PimaForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(PimaForm, self).clean()
        # validating no finger prick: options is yes, no, thats why this validation
        if cleaned_data.get('is_drawn') == 'No' and not cleaned_data.get('is_drawn_other'):
            raise forms.ValidationError('If no finger prick was done today, please explain why not?')
        return cleaned_data

    class Meta:
        model = Pima
