from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc.core.bhp_common.utils import check_initials_field
from edc.core.bhp_variables.models import StudySpecific
from edc.subject.consent.forms import BaseSubjectConsentForm
from edc.subject.registration.models import RegisteredSubject


from ..models import ClinicEligibility
from ...clinic.choices import GENDER_UNDETERMINED
from ..models import ClinicConsent


class MainConsentForm(BaseSubjectConsentForm):

    gender = forms.ChoiceField(
        label='Gender',
        choices=[choice for choice in GENDER_UNDETERMINED],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):

        cleaned_data = super(MainConsentForm, self).clean()
        try:
            obj = StudySpecific.objects.all()[0]
        except IndexError:
            raise forms.ValidationError("Please contact your DATA/IT assistant to add your edc.core.bhp_variables site specifics")

        clinic_eligibility = ClinicEligibility.objects.filter(dob=cleaned_data.get('dob'),
                                        gender=cleaned_data.get('gender'),
                                        first_name=cleaned_data.get('first_name'),
                                        initials=cleaned_data.get('initials'))
        if clinic_eligibility.exists():
            clinic_eligibility[0].match_consent_values(clinic_eligibility[0], exception_cls=forms.ValidationError)
        else:
            raise forms.ValidationError('Could not find a ClinicEligibility. Ensure \'DOB\', \'first_name\', \'gender\' and \'initials\' match those in ClinicEligibility.')

        if cleaned_data.get('is_minor') == 'Yes' and not cleaned_data.get('guardian_name', None):
            raise forms.ValidationError('You wrote subject is a minor but have not provided the guardian\'s name. Please correct.')
        if cleaned_data.get('is_minor') == 'No' and cleaned_data.get('guardian_name', None):
            raise forms.ValidationError('You wrote subject is NOT a minor. Guardian\'s name is not required for adults. Please correct.')
        # check consenting age
        if cleaned_data.get('consent_datetime'):
            consent_datetime = cleaned_data.get('consent_datetime').date()
            rdelta = relativedelta(consent_datetime, cleaned_data.get('dob'))
            if rdelta.years < obj.minimum_age_of_consent:
                raise forms.ValidationError(u'Subject is too young to consent. Got {0} years'.format(rdelta.years))
            if rdelta.years > obj.maximum_age_of_consent:
                raise forms.ValidationError(u'Subject is too old to consent. Got {0} years'.format(rdelta.years))
            if cleaned_data.get('is_minor') == 'No':
                if obj.minimum_age_of_consent <= rdelta.years < obj.age_at_adult_lower_bound:
                    raise forms.ValidationError(u'Subject is a minor based on DOB {0} yet you wrote they are not a minor. Please correct.'.format(cleaned_data.get('dob'), obj.minimum_age_of_consent, rdelta.years, obj.age_at_adult_lower_bound))
            if cleaned_data.get('is_minor') == 'Yes':
                if rdelta.years < obj.minimum_age_of_consent:
                    raise forms.ValidationError(u'Subject is minor but is too young to consent. Please correct.'.format(cleaned_data.get('dob'), obj.minimum_age_of_consent, rdelta.years, obj.age_at_adult_lower_bound))
                elif rdelta.years >= obj.age_at_adult_lower_bound:
                    raise forms.ValidationError(u'Subject is an adult based on DOB {0} yet you wrote they are a minor. Please correct.'.format(cleaned_data.get('dob'), obj.minimum_age_of_consent, rdelta.years, obj.age_at_adult_lower_bound))
                elif not (obj.minimum_age_of_consent <= rdelta.years < obj.age_at_adult_lower_bound):
                    raise forms.ValidationError(u'Subject is not a minor as defined by this protocol. Got {0} years'.format(rdelta.years))
        # check for identity
        if not cleaned_data.get('identity'):
            raise forms.ValidationError("Identity cannot be None.")
        if cleaned_data.get('identity') != cleaned_data.get('confirm_identity'):
            raise forms.ValidationError('Identity numbers do not match. Please check both the identity and your confirmation.')
        if not cleaned_data.get('identity_type'):
            raise forms.ValidationError("identity_type cannot be None.")
        # check for duplicate identity
        if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).exists():
            if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).count() > 1:
                raise forms.ValidationError("More than one subject is using this identity number. Cannot continue.")
        #check subject consent initials
        initials = cleaned_data.get("initials")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        check_initials_field(first_name, last_name, initials)

        if cleaned_data.get('have_htc_pims', None) != 'None' and not cleaned_data.get('htc_pims_id', None):
            raise forms.ValidationError('Participant reports to have either HTC, PIMS identifier or both. Please enter that identifier.')

        if cleaned_data.get('have_htc_pims', None) == 'None' and cleaned_data.get('htc_pims_id', None):
            raise forms.ValidationError('Participant reports to NOT have either HTC, PIMS identifier or both. Please DO NOT enter any identifier.')

        return cleaned_data


class ClinicConsentForm(MainConsentForm):

    class Meta:
        model = ClinicConsent
