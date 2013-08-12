from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import Pregnancy


class PregnancyForm (BaseSubjectModelForm):
    def clean(self):
        cleaned_data = super(PregnancyForm, self).clean()
        #pregnancy and antenal registration
        if cleaned_data.get('current_pregnant') == 'Yes' and not cleaned_data.get('anc_reg'):
            raise forms.ValidationError('If participant currently pregnant, have they registered for antenatal care?')
        #if currently pregnant when was the last lnmp
        if cleaned_data.get('current_pregnant') == 'Yes' and not cleaned_data.get('lnmp'):
            raise forms.ValidationError('If participant currently pregnant, when was the last known menstrual period?')
        return cleaned_data

    class Meta:
        model = Pregnancy
