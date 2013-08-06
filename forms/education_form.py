from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import Education



class EducationForm (BaseSubjectModelForm):
    
    def clean(self):

        cleaned_data = self.cleaned_data
        # validating not working
        if cleaned_data.get('job_type') == 'not working' and not cleaned_data.get('reason_unemployed'):
            raise forms.ValidationError('If participant is not working, provide reason for unemployment')
        if cleaned_data.get('job_type') != 'not working' and not cleaned_data.get('job_description'):
            raise forms.ValidationError('If participant is employed, what is the job description')
        if cleaned_data.get('job_type') != 'not working' and not cleaned_data.get('monthly_income'):
            raise forms.ValidationError('If participant is employed, what is his/her monthly income?')

        cleaned_data = super(EducationForm, self).clean()

        return cleaned_data


    class Meta:
        model = Education
