from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc.core.bhp_common.utils import check_initials_field
from edc.subject.consent.forms import BaseSubjectConsentForm
from edc.core.bhp_variables.models import StudySpecific
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp.choices import GENDER_UNDETERMINED

from ..models import SubjectConsent, SubjectConsentRbd


class MainConsentForm(BaseSubjectConsentForm):

    gender = forms.ChoiceField(
        label='Gender',
        choices=[choice for choice in GENDER_UNDETERMINED],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def check_elligibility_filled(self, cleaned_data):
        if not cleaned_data.get('household_member').eligible_subject == True:
            raise forms.ValidationError('Subject is not eligible or has not been confirmed eligible. Complete the eligibility checklist first. Got {0}'.format(cleaned_data.get('household_member')))

    def clean(self):

        cleaned_data = self.cleaned_data
        try:
            obj = StudySpecific.objects.all()[0]
        except IndexError:
            raise forms.ValidationError("Please contact your DATA/IT assistant to add your edc.core.bhp_variables site specifics")
        # check for hm
        household_member = cleaned_data.get("household_member")
        if not household_member:
            raise forms.ValidationError("HouseholdMember cannot be None.")
        if cleaned_data.get('is_minor') == 'Yes' and not cleaned_data.get('guardian_name', None):
            raise forms.ValidationError('You wrote subject is a minor but have not provided the guardian\'s name. Please correct.')
        if cleaned_data.get('is_minor') == 'No' and cleaned_data.get('guardian_name', None):
            raise forms.ValidationError('You wrote subject is NOT a minor. Guardian\'s name is not required for adults. Please correct.')
        self.check_elligibility_filled(cleaned_data)
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
        #check subject consent initials with household member initials
        if initials != household_member.initials:
            raise forms.ValidationError('Initials for household member record do not match initials here. Got {0} <> {1}'.format(household_member.initials, initials))
        #check first name matches household member
        if first_name and household_member:
            if household_member.first_name != first_name:
                raise forms.ValidationError("First name does not match. The first name recorded in the household member's information are '%s' but you wrote '%s'" % (household_member.first_name, first_name))
        #check 1st and last letters of initials match subjects name
        check_initials_field(first_name, last_name, initials)
        #check subject consent gender with household member gender
        gender = cleaned_data.get("gender", None)
        if gender and household_member:
            if household_member.gender != gender:
                raise forms.ValidationError("Gender does not match. The gender recorded in the household member's information is '%s' but you wrote '%s'" % (household_member.gender, gender))
        return super(MainConsentForm, self).clean()

    def accepted_consent_copy(self, cleaned_data):
        return True


class SubjectConsentForm(MainConsentForm):

    class Meta:
        model = SubjectConsent


class SubjectConsentRbdForm(MainConsentForm):

    class Meta:
        model = SubjectConsentRbd
