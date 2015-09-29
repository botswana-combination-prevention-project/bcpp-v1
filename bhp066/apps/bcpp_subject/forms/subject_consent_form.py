from django import forms
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned

from edc.map.classes import site_mappers
from edc.subject.registration.models import RegisteredSubject
from edc_consent.forms.base_consent_form import BaseConsentForm
from edc_constants.constants import NOT_APPLICABLE, NO, YES

from bhp066.apps.bcpp_household.constants import BASELINE_SURVEY_SLUG
from bhp066.apps.bcpp_household_member.constants import HEAD_OF_HOUSEHOLD
from bhp066.apps.bcpp_household_member.models import HouseholdInfo
from bhp066.apps.bcpp_survey.models import Survey

from ..models import SubjectConsent, SubjectConsentExtended
from copy import deepcopy


class BaseBcppConsentForm(BaseConsentForm):

    def clean(self):
        cleaned_data = super(BaseBcppConsentForm, self).clean()
        self.clean_consent_with_household_member()
        self.clean_citizen_with_legally_married()
        self.limit_edit_to_current_community()
        self.limit_edit_to_current_survey()
        self.household_info()
        try:
            model = self._meta.model.proxy_for_model
        except AttributeError:
            model = self._meta.model
        household_member = cleaned_data.get('household_member')
        if household_member:
            subject_consent = model(**cleaned_data)
            subject_consent.matches_enrollment_checklist(
                subject_consent, household_member, exception_cls=forms.ValidationError)
        return cleaned_data

    def clean_consent_matches_enrollment(self):
        household_member = self.cleaned_data.get("household_member")
        if not SubjectConsent.objects.filter(
                household_member__internal_identifier=household_member.internal_identifier).exclude(
                household_member=household_member).exists():
            consent_datetime = self.cleaned_data.get("consent_datetime", self.instance.consent_datetime)
            options = deepcopy(self.cleaned_data)
            options.update({'consent_datetime': consent_datetime})
            self.instance.matches_enrollment_checklist(
                SubjectConsent(**options), household_member, forms.ValidationError)
            self.instance.matches_hic_enrollment(
                SubjectConsent(**options), household_member, forms.ValidationError)

    def clean_consent_with_household_member(self):
        """Validates subject consent values against household member values."""
        initials = self.cleaned_data.get("initials")
        first_name = self.cleaned_data.get("first_name")
        gender = self.cleaned_data.get("gender")
        household_member = self.cleaned_data.get("household_member")
        if household_member:
            if initials != household_member.initials:
                raise forms.ValidationError(
                    'Initials do not match with household member. %(initials)s <> %(hm_initials)s',
                    params={'hm_initials': household_member.initials, 'initials': initials},
                    code='invalid')
            if household_member.first_name != first_name:
                raise forms.ValidationError(
                    'First name does not match with household member. Got %(first_name)s <> %(hm_first_name)s',
                    params={'hm_first_name': household_member.first_name, 'first_name': first_name},
                    code='invalid')
            if household_member.gender != gender:
                raise forms.ValidationError(
                    'Gender does not match with household member. Got %(gender)s <> %(hm_gender)s',
                    params={'hm_gender': household_member.gender, 'gender': gender},
                    code='invalid')

    def clean_citizen_with_legally_married(self):
        citizen = self.cleaned_data.get('citizen')
        legal_marriage = self.cleaned_data.get('legal_marriage')
        marriage_certificate = self.cleaned_data.get('marriage_certificate')
        if citizen == NO:
            if legal_marriage == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen. Is the subject legally married to a citizen?',
                    code='invalid')
            elif legal_marriage == NO:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen and is NOT legally married to a citizen. '
                    'Subject cannot be consented',
                    code='invalid')
            elif legal_marriage == YES and marriage_certificate != YES:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen. Subject needs to produce a marriage certificate',
                    code='invalid')
        if citizen == YES:
            if legal_marriage != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is a citizen. That subject is legally married to a citizen is not applicable.',
                    code='invalid')
            elif marriage_certificate != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is a citizen. The subject\'s marriage certificate is not applicable.',
                    code='invalid')

    def limit_edit_to_current_survey(self):
        household_member = self.cleaned_data.get("household_member")
        if household_member:
            try:
                limit = settings.LIMIT_EDIT_TO_CURRENT_SURVEY
            except AttributeError:
                limit = False
            if limit:
                current_survey = Survey.objects.current_survey()
                if household_member.household_structure.survey != current_survey:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from %(current_survey)s '
                        'may be added/changed. (LIMIT_EDIT_TO_CURRENT_SURVEY)',
                        params={'current_survey': current_survey},
                        code='invalid')

    def limit_edit_to_current_community(self):
        household_member = self.cleaned_data.get("household_member")
        if household_member:
            try:
                limit = settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY
            except AttributeError:
                limit = False
            if limit:
                mapper_community = site_mappers.get_current_mapper().map_area
                community = household_member.household_structure.household.plot.community
                if community != mapper_community:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from \'%(mapper_community)s\' may be added/changed on '
                        'this device. Got %(community)s. (LIMIT_EDIT_TO_CURRENT_COMMUNITY)',
                        params={'mapper_community': mapper_community, 'community': community}, code='invalid')

    def household_info(self):
        household_member = self.cleaned_data.get('household_member')
        if household_member:
            if (household_member.relation == HEAD_OF_HOUSEHOLD and
                    household_member.household_structure.survey.survey_slug == BASELINE_SURVEY_SLUG):
                try:
                    HouseholdInfo.objects.get(household_member=household_member)
                except HouseholdInfo.DoesNotExist:
                    raise forms.ValidationError(
                        'Complete \'%(model)s\' before consenting head of household',
                        params={'model': HouseholdInfo._meta.verbose_name}, code='invalid')

    def clean_household_member(self):
        household_member = self.cleaned_data.get("household_member")
        if not household_member:
            raise forms.ValidationError("Please select the household member.")
        return household_member

    def clean_identity(self):
        try:
            identity = super(BaseBcppConsentForm, self).clean_identity()
        except AttributeError:
            identity = self.cleaned_data.get('identity')
        try:
            RegisteredSubject.objects.get(identity=identity)
        except MultipleObjectsReturned:
            raise forms.ValidationError(
                "More than one subject is using this identity number. Cannot continue.",
                code='invalid')
        except RegisteredSubject.DoesNotExist:
            pass
        return identity


class SubjectConsentForm(BaseBcppConsentForm):

    class Meta:
        model = SubjectConsent


class SubjectConsentExtendedForm(BaseBcppConsentForm):

    class Meta:
        model = SubjectConsentExtended
