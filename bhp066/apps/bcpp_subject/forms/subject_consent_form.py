from datetime import date
from dateutil.relativedelta import relativedelta

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

# from edc.core.bhp_variables.models import StudySpecific
from edc.map.classes import site_mappers
from edc.subject.registration.models import RegisteredSubject

from bhp066.apps.bcpp.choices import GENDER_UNDETERMINED
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household_member.models import HouseholdInfo
from bhp066.apps.bcpp_household.constants import BASELINE_SURVEY_SLUG

from ..models import SubjectConsent

from .base_subject_consent_form import BaseSubjectConsentForm


class BaseBcppConsentForm(BaseSubjectConsentForm):  # TODO: LOOK AT THE CLEAN METHOD IN BASE!!

    gender = forms.ChoiceField(
        label='Gender',
        choices=[choice for choice in GENDER_UNDETERMINED],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(BaseBcppConsentForm, self).clean()
#         try:
#             instance = self.instance
#         except AttributeError:
#             instance = self.model(**cleaned_data)
        household_member = cleaned_data.get("household_member", '')
        if not household_member:
            raise forms.ValidationError("Please select the household member.")

        # self.study_specifics_checks(cleaned_data.get('dob'))  (handled using a validator)

        # check for duplicate identity
        if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).exists():
            if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).count() > 1:
                raise forms.ValidationError("More than one subject is using this identity number. Cannot continue.")

        # check subject consent values against household member values
        initials = cleaned_data.get("initials")
        first_name = cleaned_data.get("first_name")
        if initials != household_member.initials:
            raise forms.ValidationError('Initials for household member record do not match initials here. Got {0} <> {1}'.format(household_member.initials, initials))
        if first_name and household_member:
            if household_member.first_name != first_name:
                raise forms.ValidationError("First name does not match. The first name recorded in the household member's information are '%s' but you wrote '%s'" % (household_member.first_name, first_name))
#         if last_name and household_member:
#             if household_member.last_name != last_name:
#                 raise forms.ValidationError("Last name does not match. The last name recorded in the household member's information are '%s' but you wrote '%s'" % (household_member.last_name, last_name))
        gender = cleaned_data.get("gender", None)
        if gender and household_member:
            if household_member.gender != gender:
                raise forms.ValidationError("Gender does not match. The gender recorded in the household member's information is '%s' but you wrote '%s'" % (household_member.gender, gender))
        return cleaned_data

    def age(self, dob):
        return relativedelta(date.today(), dob).years

#     def study_specifics_checks(self, dob):
#         age_settings = StudySpecific.objects.all()[0]
#         age = relativedelta(date.today(), dob).years
#         if age < age_settings.minimum_age_of_consent:
#             raise forms.ValidationError(u'Subject is too young to consent. Got {0} years'.format(age))
#         if age > age_settings.maximum_age_of_consent:
#             raise forms.ValidationError(u'Subject is too old to consent. Got {0} years'.format(age))


class SubjectConsentForm(BaseBcppConsentForm):

    def clean(self):
        cleaned_data = super(SubjectConsentForm, self).clean()
        household_member = cleaned_data.get("household_member")
        self.limit_edit_to_current_community(household_member)
        self.limit_edit_to_current_survey(household_member)
        self.household_info(household_member)
        options = cleaned_data
        if 'consent_datetime' not in cleaned_data:
            options.update({'consent_datetime': self.instance.consent_datetime})
        if not SubjectConsent.objects.filter(
                household_member__internal_identifier=cleaned_data.get('household_member').internal_identifier).exclude(
                household_member=cleaned_data.get('household_member')).exists():
            self.instance.matches_enrollment_checklist(
                SubjectConsent(**options), cleaned_data.get('household_member'), forms.ValidationError)
            self.instance.matches_hic_enrollment(
                SubjectConsent(**options), cleaned_data.get('household_member'), forms.ValidationError)
        return cleaned_data

    def limit_edit_to_current_survey(self, household_member):
        try:
            if settings.LIMIT_EDIT_TO_CURRENT_SURVEY:
                current_survey = Survey.objects.current_survey()
                if household_member.household_structure.survey != current_survey:
                    raise forms.ValidationError('Form may not be saved. Only data from {} '
                                                'may be added/changed. (LIMIT_EDIT_TO_CURRENT_SURVEY)'
                                                ).format(current_survey)
        except AttributeError:
            pass

    def limit_edit_to_current_community(self, household_member):
        try:
            if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
                configured_community = site_mappers.get_current_mapper().map_area
                community = household_member.household_structure.household.plot.community
                if community != configured_community:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from \'{}\' may be added/changed on '
                        'this device. Got {}. (LIMIT_EDIT_TO_CURRENT_COMMUNITY)'.format(
                            configured_community, community))
        except AttributeError:
            pass

    def household_info(self, household_member):
        try:
            if (household_member.relation == 'Head' and
                    household_member.household_structure.survey.survey_slug == BASELINE_SURVEY_SLUG):
                HouseholdInfo.objects.get(household_member=household_member)
        except HouseholdInfo.DoesNotExist:
            raise forms.ValidationError(
                'Complete \'{}\' before consenting head of household'.format(HouseholdInfo._meta.verbose_name))

    class Meta:
        model = SubjectConsent
