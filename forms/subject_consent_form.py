from datetime import date
from django import forms
from django.core.exceptions  import ObjectDoesNotExist
from bhp_common.utils import formatted_age
from bhp_common.utils import check_initials_field
from bhp_consent.forms import BaseSubjectConsentForm
from dateutil.relativedelta import relativedelta
from bhp_variables.models import StudySpecific
from bhp_registration.models import RegisteredSubject
from bcpp_survey.models import Survey
from bcpp_household.models import HouseholdStructureMember
from bcpp_subject.models import SubjectConsentYearOne, SubjectConsentYearTwo, SubjectConsentYearThree, SubjectConsentYearFour, SubjectConsentYearFive


class MyBaseSubjectConsentForm(BaseSubjectConsentForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        if 'is_minor' in cleaned_data:
            if cleaned_data.get('is_minor') == 'Yes' and not cleaned_data.get('guardian_name', None):
                raise forms.ValidationError('You wrote subject is a minor but have not provided the guardian\'s name. Please correct.')
            if cleaned_data.get('is_minor') == 'No' and cleaned_data.get('guardian_name', None):
                raise forms.ValidationError('You wrote subject is NOT a minor. Guardian\'s name is not required for adults. Please correct.')

            #repeat validation on dob against is_minor YES/NO
            try:
                obj = StudySpecific.objects.all()[0]
            except IndexError:
                raise TypeError("Please add your bhp_variables site specifics")
            if cleaned_data.get('consent_datetime', None):
                consent_datetime = cleaned_data.get('consent_datetime').date()
            else:
                consent_datetime = date.today()
            rdelta = relativedelta(consent_datetime, cleaned_data.get('dob'))
            if cleaned_data.get('is_minor') == 'No' and (rdelta.years >= obj.minimum_age_of_consent and rdelta.years < obj.age_at_adult_lower_bound):
                raise forms.ValidationError(u'Subject is a minor based on DOB {0} yet you wrote they are not a minor. Please correct.'.format(cleaned_data.get('dob')))
            if cleaned_data.get('is_minor') == 'Yes' and not (rdelta.years >= obj.minimum_age_of_consent and rdelta.years < obj.age_at_adult_lower_bound):
                raise forms.ValidationError(u'Subject is an adult based on DOB {0} yet you wrote they are a minor. Please correct.'.format(cleaned_data.get('dob')))
        if cleaned_data.get('identity') != cleaned_data.get('confirm_identity'):
            raise forms.ValidationError('Identity numbers do not match. Please check both the identity and your confirmation.')
        report_datetime = cleaned_data.get('consent_datetime')
        survey = cleaned_data.get('survey')
        household_structure_member = cleaned_data.get("household_structure_member")
        if not household_structure_member:
            raise forms.ValidationError("HouseholdStructureMember cannot be None.")
        identity_type = cleaned_data.get('identity_type')
        if not identity_type:
            raise forms.ValidationError("identity_type cannot be None.")
        household_identifier = household_structure_member.household_structure.household.household_identifier
        if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).exists():
            if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).count() > 1:
                raise forms.ValidationError("More than one subject is using this identity number. Cannot continue.")
            registered_subject = RegisteredSubject.objects.get(identity=cleaned_data.get('identity'))
            previous_household_structure_member = HouseholdStructureMember.objects.filter(pk=registered_subject.registration_identifier)
            if previous_household_structure_member:
                if not previous_household_structure_member[0].household_structure.household.household_identifier == household_identifier:
                        raise forms.ValidationError("Subject not found in {0} for this registered subject / omang'.".format(household_identifier))
        #check date of consent is within survey start and end dates
        if survey:
            if not (survey.datetime_start - report_datetime).days >= 0 and not (report_datetime - survey.datetime_end).days <= 0:
                raise forms.ValidationError('Consent cannot be for survey %s. Survey %s starts on %s and ends on %s. Your wrote %s' % (survey.survey_name, survey.survey_name, survey.datetime_start.date(), survey.datetime_end.date(), report_datetime.date()))

        #check subjectconsent initials with householdstructuremember initials
        my_initials = cleaned_data.get("initials")
        my_first_name = cleaned_data.get("first_name")
        my_last_name = cleaned_data.get("last_name")

        check_initials_field(my_first_name, my_last_name, my_initials)

        #check first name matches householdstructuremember
        if my_first_name and household_structure_member:
            if household_structure_member.first_name != my_first_name:
                raise forms.ValidationError("First name does not match. The first name recorded in the household member's information are '%s' but you wrote '%s'" % (household_structure_member.first_name, my_first_name))

        #check 1st and last letters of initials match subjects name
        check_initials_field(my_first_name, my_last_name, my_initials)

        #check subjectconsent gender with householdstructuremember gender
        my_gender = cleaned_data.get("gender", None)
        if my_gender and household_structure_member:
            if household_structure_member.gender != my_gender:
                raise forms.ValidationError("Gender does not match. The gender recorded in the household member's information is '%s' but you wrote '%s'" % (household_structure_member.gender, my_gender))
        return super(MyBaseSubjectConsentForm, self).clean()


class SubjectConsentYearOneForm(MyBaseSubjectConsentForm):
    try:
        survey = Survey.objects.get(survey_slug='bcpp-year-1')
    except:
        survey = None

    class Meta:
        model = SubjectConsentYearOne
        exclude = ('assessment_score', 'is_minor', )


class SubjectConsentYearTwoForm(MyBaseSubjectConsentForm):
    try:
        survey = Survey.objects.get(survey_slug='bcpp-year-2')
    except:
        survey = None

    class Meta:
        model = SubjectConsentYearTwo


class SubjectConsentYearThreeForm(MyBaseSubjectConsentForm):
    try:
        survey = Survey.objects.get(survey_slug='bcpp-year-3')
    except:
        survey = None

    class Meta:
        model = SubjectConsentYearThree


class SubjectConsentYearFourForm(MyBaseSubjectConsentForm):
    try:
        survey = Survey.objects.get(survey_slug='bcpp-year-4')
    except:
        survey = None

    class Meta:
        model = SubjectConsentYearFour


class SubjectConsentYearFiveForm(MyBaseSubjectConsentForm):
    try:
        survey = Survey.objects.get(survey_slug='bcpp-year-5')
    except:
        survey = None

    class Meta:
        model = SubjectConsentYearFive
