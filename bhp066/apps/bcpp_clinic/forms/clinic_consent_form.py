from dateutil.relativedelta import relativedelta

from django import forms
# from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc.core.bhp_common.utils import check_initials_field
from edc.core.bhp_variables.models import StudySpecific
from edc.subject.consent.forms import BaseSubjectConsentForm
from edc.subject.registration.models import RegisteredSubject

# from apps.clinic.choices import GENDER_UNDETERMINED

from ..models import ClinicConsent
from ..models import ClinicEligibility


class ClinicConsentForm(BaseSubjectConsentForm):

    def clean(self):

        cleaned_data = super(ClinicConsentForm, self).clean()

        try:
            clinic_eligibility = ClinicEligibility.objects.get(
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
