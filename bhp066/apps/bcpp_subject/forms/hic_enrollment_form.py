from django import forms
from ..models import HicEnrollment, ResidencyMobility, HivResult, SubjectConsent, SubjectLocator
from .base_subject_model_form import BaseSubjectModelForm


class HicEnrollmentForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        # validating a need to specify the participant's preference
        if not cleaned_data.get('subject_visit', None).household_member:
            raise forms.ValidationError('This form has to be attached by to a household member. Currently it is not.')
        mobility = ResidencyMobility.objects.filter(subject_visit=cleaned_data.get('subject_visit'))
        if mobility.exists():
            if mobility[0].intend_residency == 'Yes':
                raise forms.ValidationError('In Recidency Mobility form this individual states they want to move out of this community. Please cancel and revise that answer before coming back to this HicEnrollment form.')
            if mobility[0].permanent_resident != 'Yes':
                raise forms.ValidationError('In Recidency Mobility form this individual has to spend atleast 14 days/month. Please cancel and revise that answer before coming back to this HicEnrollment form.')
        else:
            raise forms.ValidationError('You need to have filled the Recidency Mobility form before this one.')
        hiv_result = HivResult.objects.filter(subject_visit=cleaned_data.get('subject_visit'))
        if hiv_result.exists():
            if hiv_result[0].hiv_result.lower() != 'neg':
                raise forms.ValidationError('This participant needs to be \'NEG\' in Today\'s HivResult form. Please review that answer before continuing with this form.')
        else:
            raise forms.ValidationError('You need to have filled the Today\'s HivResult form before this one.')
        #Validations below commented out because those fields are readonly, hence not submitted with the form. Its sufficient to validate them in the save method.
#         subject_consent = SubjectConsent.objects.filter(household_member = cleaned_data.get('subject_visit').household_member)
#         if subject_consent.exists():
#             if subject_consent[0].dob != cleaned_data.get('dob') or subject_consent[0].consent_datetime != cleaned_data.get('consent_datetime'):
#                 raise forms.ValidationError('The \'dob\' or \'consent_datetime\' in this form do not match those in the subject consent. Please review that answer before continuing with this form.')
#             #Dont need to check for citizen or non citizen married to citizen with valid certificate because a consent will never save withou that consition being TRUE.
#         else:
#             raise forms.ValidationError('You need to have filled the SubjectConsent form before this one.')
#         subject_locator = SubjectLocator.objects.filter(subject_visit = cleaned_data.get('subject_visit'))
#         if subject_locator.exists():
#             if not subject_locator[0].subject_cell and not subject_locator[0].subject_cell_alt and not subject_locator[0].subject_phone:
#                 raise forms.ValidationError('There has to be atleast one of \'subject_cell\', \'subject_cell_alt\' or \'subject_phone\' in SubjectLocator. Please review that answer before continuing with this form.')
#         else:
#             raise forms.ValidationError('You need to have filled the SubjetLocator form before this one.')
        return super(HicEnrollmentForm, self).clean()

    class Meta:
        model = HicEnrollment
