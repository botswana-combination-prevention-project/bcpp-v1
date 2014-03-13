from django import forms
from ..models import HicEnrollment, ResidencyMobility, HivResult
from .base_subject_model_form import BaseSubjectModelForm


class HicEnrollmentForm (BaseSubjectModelForm):

    def clean(self):

        cleaned_data = super(HicEnrollmentForm, self).clean()
        # validating a need to specify the participant's preference
        mobility = ResidencyMobility.objects.filter(subject_visit=cleaned_data.get('subject_visit'))
        if mobility.exists():
            if mobility[0].intend_residency == 'Yes':
                raise forms.ValidationError('In Recidency Mobility form this individual states they want to move out of this community. Please cancel and revise that answer before coming back to this HicEnrollment form.')
            if mobility[0].permanent_resident != 'Yes':
                raise forms.ValidationError('In Recidency Mobility form this individual has to spend atleast 14 days/month. Please cancel and revise that answer before coming back to this HicEnrollment form.')
        else:
            raise forms.ValidationError('You need to have filled the Recidency Mobility form before this one.')
        hiv_result = HivResult.objects.filter(subject_visit=cleaned_data.get('subject_visit'))
        if not hiv_result.exists():
            raise forms.ValidationError('You need to have filled the Today\'s HivResult form before this one.')

        return cleaned_data

    class Meta:
        model = HicEnrollment
