from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import SexualBehaviour


class SexualBehaviourForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        #if respondent has had sex, answer all following questions on form
        if cleaned_data.get('last_sex') == 'Days' and not cleaned_data.get('last_sex_calc'):
            raise forms.ValidationError('If participant has had sex, and indicated a time point when last had sex, provide number of days')
        if cleaned_data.get('last_sex') == 'Months' and not cleaned_data.get('last_sex_calc'):
            raise forms.ValidationError('If participant has had sex, and indicated a time point when last had sex, provide number of months')
        if cleaned_data.get('last_sex') == 'Years' and not cleaned_data.get('last_sex_calc'):
            raise forms.ValidationError('If participant has had sex, and indicated a time point when last had sex, provide number of years')
        
        cleaned_data = super(SexualBehaviourForm, self).clean()
        return cleaned_data

    class Meta:
        model = SexualBehaviour
        