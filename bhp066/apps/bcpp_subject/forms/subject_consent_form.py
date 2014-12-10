from datetime import date
from dateutil.relativedelta import relativedelta

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc.subject.consent.forms import BaseSubjectConsentForm
from edc.core.bhp_variables.models import StudySpecific
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp.choices import GENDER_UNDETERMINED
from apps.bcpp_survey.models import Survey

from ..models import SubjectConsent


class BaseBcppConsentForm(BaseSubjectConsentForm):  # TODO: LOOK AT THE CLEAN METHOD IN BASE!!

    gender = forms.ChoiceField(
        label='Gender',
        choices=[choice for choice in GENDER_UNDETERMINED],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = super(BaseBcppConsentForm, self).clean()

        household_member = cleaned_data.get("household_member")

        if not household_member:
            raise forms.ValidationError("Please select the household member.")

        self.study_specifics_checks(cleaned_data.get('dob'))

        # check for duplicate identity
        if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).exists():
            if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).count() > 1:
                raise forms.ValidationError("More than one subject is using this identity number. Cannot continue.")

        # check subject consent values against household member values
        initials = cleaned_data.get("initials")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
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

    def study_specifics_checks(self, dob):
        age_settings = StudySpecific.objects.all()[0]
        age = relativedelta(date.today(), dob).years
        if age < age_settings.minimum_age_of_consent:
            raise forms.ValidationError(u'Subject is too young to consent. Got {0} years'.format(age))
        if age > age_settings.maximum_age_of_consent:
            raise forms.ValidationError(u'Subject is too old to consent. Got {0} years'.format(age))


class SubjectConsentForm(BaseBcppConsentForm):

    def clean(self):
        cleaned_data = super(SubjectConsentForm, self).clean()
        self.limit_edit_to_current_survey(cleaned_data)
        options = cleaned_data
        if 'consent_datetime' not in cleaned_data:
            options.update({'consent_datetime': self.instance.consent_datetime})
        self.instance.matches_enrollment_checklist(SubjectConsent(**options), cleaned_data.get('household_member'), forms.ValidationError)
        self.instance.matches_hic_enrollment(SubjectConsent(**options), cleaned_data.get('household_member'), forms.ValidationError)
        return cleaned_data

    def limit_edit_to_current_survey(self, cleaned_data):
        household_member = cleaned_data.get("household_member")
        try:
            if settings.LIMIT_EDIT_TO_CURRENT_SURVEY:
                current_survey = Survey.objects.current_survey
                if household_member.household_structure.survey == current_survey:
                    raise forms.ValidationError('Form may not be saved. Only data from {} '
                                                'may be added/changed. (LIMIT_EDIT_TO_CURRENT_SURVEY)'
                                                ).format(current_survey)
        except AttributeError:
            pass


    class Meta:
        model = SubjectConsent
