from django import forms

from ..models import Education, SubjectLocator

from .base_subject_model_form import BaseSubjectModelForm


class EducationForm (BaseSubjectModelForm):

    def clean(self):
        cleaned_data = super(EducationForm, self).clean()
        # validating not working
        try:
            subject_locator = SubjectLocator.objects.get(subject_visit=cleaned_data.get('employed'))
            if subject_locator.may_call_work == 'Yes' and cleaned_data.get('working') == 'No':
                raise forms.ValidationError(
                    'Participant gave permission to be contacted at WORK in the subject locator, \
                    but now reports to be \'Not Working\'. Either correct this form or change answer in the Locator')
        except SubjectLocator.DoesNotExist:
            pass
        if cleaned_data.get('working', None) == 'No' and cleaned_data.get('job_type', None):
            raise forms.ValidationError('If participant is not working, do not give job type')
        if cleaned_data.get('working', None) == 'No' and cleaned_data.get('job_description', None):
            raise forms.ValidationError('Participant is not working, please do not provide any job description')
        # give reason for unemployment
        if cleaned_data.get('working', None) == 'No' and not cleaned_data.get('reason_unemployed', None):
            raise forms.ValidationError('If participant is not working, provide reason for unemployment')
        # retirement
        if cleaned_data.get('reason_unemployed', None) == 'retired' and not cleaned_data.get('monthly_income', None):
            raise forms.ValidationError('If participant is retired, how much of the retirement benefit is received monthly?')
        # student/apprentice/volunteer
        if cleaned_data.get('reason_unemployed', None) == 'student' and not cleaned_data.get('monthly_income', None):
            raise forms.ValidationError('If participant is student/apprentice/volunteer, how much payment is received monthly?')
        # validating for those employed
        if cleaned_data.get('working', None) == 'Yes' and cleaned_data.get('reason_unemployed', None):
            raise forms.ValidationError('You have provided unemployment details yet have indicated that participant is working')
        if cleaned_data.get('working', None) == 'Yes' and not cleaned_data.get('job_type', None):
            raise forms.ValidationError('If participant is working, provide the job type')
        if cleaned_data.get('working', None) == 'Yes' and not cleaned_data.get('job_description', None):
            raise forms.ValidationError('If participant is employed, what is the job description')
        if cleaned_data.get('working', None) == 'Yes' and not cleaned_data.get('monthly_income', None):
            raise forms.ValidationError('If participant is employed, what is his/her monthly income?')
        return cleaned_data

    class Meta:
        model = Education
