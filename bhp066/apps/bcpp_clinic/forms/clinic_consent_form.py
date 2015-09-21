from django import forms

from edc_consent.forms import BaseSubjectConsentForm

from ..models import ClinicConsent, ClinicEligibility


class ClinicConsentForm(BaseSubjectConsentForm):

    def clean(self):

        cleaned_data = super(ClinicConsentForm, self).clean()

        try:
            ClinicEligibility.objects.get(
                dob=cleaned_data.get('dob'),
                gender=cleaned_data.get('gender'),
                first_name=cleaned_data.get('first_name'),
                initials=cleaned_data.get('initials'),
                identity=cleaned_data.get('identity')
            )
        except ClinicEligibility.DoesNotExist:
            raise forms.ValidationError('Could not find a matching eligibility checklist. '
                                        'Ensure \'DOB\', \'first_name\', \'gender\', \'initials\' '
                                        'and \'identity\' match those on this member\'s eligibility checklist.')

        # clinic_eligibility.match_consent_values(clinic_eligibility, exception_cls=forms.ValidationError)

        return cleaned_data

    class Meta:
        model = ClinicConsent
