from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import BloodDraw


class BloodDrawForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(BloodDrawForm, self).clean()
        if cleaned_data.get('is_blood_drawn', None) == 'No' and not cleaned_data.get('is_blood_drawn_other'):
            raise forms.ValidationError('If blood was not drawn today, please explain why')
        if cleaned_data.get('is_blood_drawn', None) == 'Yes' and cleaned_data.get('is_blood_drawn_other', None):
            raise forms.ValidationError('If blood WAS drawn today, please do not provide an explanation.')
        if cleaned_data.get('is_blood_drawn', None) == 'Yes' and not cleaned_data.get('draw_date'):
            raise forms.ValidationError('If blood was drawn today, please provide the date and time of the blood draw')
        if cleaned_data.get('is_blood_drawn', None) == 'No' and cleaned_data.get('draw_date', None):
            raise forms.ValidationError('If blood was not drawn today, please do not provide the date and time of the blood draw')
        if cleaned_data.get('record_available') == 'Yes' and not cleaned_data.get('last_cd4_count') and not cleaned_data.get('last_cd4_drawn_date'):
            raise forms.ValidationError('If last known record of CD4 count is available or known, please provide the CD4 count and the CD4 date')
        if cleaned_data.get('record_available') == 'No' and (cleaned_data.get('last_cd4_count', None) or cleaned_data.get('last_cd4_drawn_date', None)):
            raise forms.ValidationError('If last known record of CD4 count is not available or not known, please do NOT provide the CD4 count and the CD4 date')
        return cleaned_data

    class Meta:
        model = BloodDraw
