from django import forms

from ..models import ReproductiveHealth

from .base_subject_model_form import BaseSubjectModelForm


class ReproductiveHealthForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(ReproductiveHealthForm, self).clean()
        if cleaned_data.get('menopause') == 'Yes' and cleaned_data.get('family_planning'):
            raise forms.ValidationError('if participant has reached menopause, you should not be giving details about family planning')
        if cleaned_data.get('menopause') == 'Yes' and  cleaned_data.get('currently_pregnant'):
            raise forms.ValidationError('If participant has reached menopause, do not give details about current pregnancy')
        if cleaned_data.get('menopause') == 'No' and not cleaned_data.get('family_planning'):
            raise forms.ValidationError('if participant has not reached menopause, provide the family planning details')
        if cleaned_data.get('menopause') == 'No' and  not cleaned_data.get('currently_pregnant'):
            raise forms.ValidationError('If participant has not reached menopause, we need to know if participant is currently pregnant or not.')
        return cleaned_data

    class Meta:
        model = ReproductiveHealth
