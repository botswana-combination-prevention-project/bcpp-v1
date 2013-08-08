from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import BloodDraw


class BloodDrawForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        
        if cleaned_data.get('is_blood_drawn') == 'No' and not cleaned_data.get('is_blood_drawn_other'):
            raise forms.ValidationError('If blood was not drawn today, please explain why')
        if cleaned_data.get('is_blood_drawn') == 'Yes' and not cleaned_data.get('draw_date'):
            raise forms.ValidationError('If blood was drawn today, please provide the date and time of the blood draw')
        if cleaned_data.get('record_available') == 'Yes' and not cleaned_data.get('last_cd4_count') and not cleaned_data.get('last_cd4_drawn_date'):
            raise forms.ValidationError('If last known record of CD4 count is available or known, please provide the CD4count and the CD4date')


        cleaned_data = super(BloodDrawForm, self).clean()

        return cleaned_data

    class Meta:
        model = BloodDraw
