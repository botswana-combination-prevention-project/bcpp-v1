from datetime import date
from dateutils import relativedelta

from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from edc.core.bhp_common.utils import check_initials_field
from edc.subject.consent.forms import BaseSubjectConsentForm
from edc.core.bhp_variables.models import StudySpecific
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp.choices import GENDER_UNDETERMINED
from apps.bcpp_household_member.models import EnrolmentChecklist

from ..models import SubjectConsent, HicEnrollment


class BaseBcppConsentForm(BaseSubjectConsentForm):  # TODO: LOOK AT THE CLEAN METHOD IN BASE!!

    gender = forms.ChoiceField(
        label='Gender',
        choices=[choice for choice in GENDER_UNDETERMINED],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    def clean(self):
        cleaned_data = self.cleaned_data
        household_member = cleaned_data.get("household_member")
        self.check_eligibility_filled(cleaned_data)
        self.study_specifics_checks(cleaned_data.get('dob'))
#         # check for identity
#         if not cleaned_data.get('identity'):
#             raise forms.ValidationError("Identity cannot be None.")
#         if cleaned_data.get('identity') != cleaned_data.get('confirm_identity'):
#             raise forms.ValidationError('Identity numbers do not match. Please check both the identity and your confirmation.')
#         if not cleaned_data.get('identity_type'):
#             raise forms.ValidationError("identity_type cannot be None.")
        #Check legal marriage for non-citizens
        if cleaned_data.get('citizen', None).lower() == 'yes' and (cleaned_data.get('legal_marriage', None) != 'N/A' or cleaned_data.get('marriage_certificate_no', None)):
            raise forms.ValidationError("For a citizen, legal marriage, marriage certificate should be Not Applicable and marriage certificate No. blank. ")
        if cleaned_data.get('citizen', None).lower() == 'no' and cleaned_data.get('legal_marriage', None).lower() != 'yes' and not cleaned_data.get('marriage_certificate_no', None):
            raise forms.ValidationError("For a non citizen, legal marriage to a citizen with a valid certificate is required.")
        # check for duplicate identity
        if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).exists():
            if RegisteredSubject.objects.filter(identity=cleaned_data.get('identity')).count() > 1:
                raise forms.ValidationError("More than one subject is using this identity number. Cannot continue.")
#         #check subject consent initials
        initials = cleaned_data.get("initials")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if initials != household_member.initials:
            raise forms.ValidationError('Initials for household member record do not match initials here. Got {0} <> {1}'.format(household_member.initials, initials))
        if first_name and household_member:
            if household_member.first_name != first_name:
                raise forms.ValidationError("First name does not match. The first name recorded in the household member's information are '%s' but you wrote '%s'" % (household_member.first_name, first_name))
        #check subject consent gender with household member gender
        gender = cleaned_data.get("gender", None)
        if gender and household_member:
            if household_member.gender != gender:
                raise forms.ValidationError("Gender does not match. The gender recorded in the household member's information is '%s' but you wrote '%s'" % (household_member.gender, gender))
        return super(BaseBcppConsentForm, self).clean()

    def enrollment_checklist_checks(self, enrollment_checklist, cleaned_data, obj):
        minor = obj.minimum_age_of_consent <= self.calculate_age(cleaned_data.get('dob', None)) < obj.age_at_adult_lower_bound
        if enrollment_checklist.dob != cleaned_data.get('dob', None):
            raise forms.ValidationError('Dob in this consent does not match that in the enrollment checklist')
        if enrollment_checklist.initials != cleaned_data.get('initials', None):
            raise forms.ValidationError('Initials in this consent does not match that in the enrollment checklist')
        if enrollment_checklist.guardian.lower() == 'yes' and not (minor and cleaned_data.get('guardian_name', None)):
            raise forms.ValidationError('Enrollment checklist indicates that subject is a minor with guardian available, but the consent does not indicate this.')
        if enrollment_checklist.gender != cleaned_data.get('gender', None):
            raise forms.ValidationError('Gender in this consent does not match that in the enrollment checklist')
        if enrollment_checklist.citizen != cleaned_data.get('citizen', None):
            raise forms.ValidationError('Enrollment checklist indicates that this subject is a citizen, but the consent does not indicate this.')
        if (enrollment_checklist.legal_marriage.lower() == 'yes' and enrollment_checklist.marriage_certificate.lower() == 'yes') and not \
            (cleaned_data.get('legal_marriage', None).lower() == 'yes' and cleaned_data.get('marriage_certificate', None).lower() == 'yes'):
                raise forms.ValidationError('Enrollment checklist indicates that this subject is married to a citizen with a valid marriage certificate, but the consent does not indicate this.')

    def check_eligibility_filled(self, cleaned_data):  # Defaults to BHS eligibility
        if not cleaned_data.get('household_member').eligible_subject:
            raise forms.ValidationError('Subject is not eligible or has not been confirmed eligible. Complete the eligibility checklist first. Got {0}'.format(cleaned_data.get('household_member')))

    def age(self, dob):
        return relativedelta(date.today(), dob).years

    def study_specifics_checks(self, dob):
        age_settings = StudySpecific.objects.all()[0]
        age = relativedelta(date.today(), dob).years
        if age < age_settings.minimum_age_of_consent:
            raise forms.ValidationError(u'Subject is too young to consent. Got {0} years'.format(age))
        if age > age_settings.maximum_age_of_consent:
            raise forms.ValidationError(u'Subject is too old to consent. Got {0} years'.format(age))

    def accepted_consent_copy(self, cleaned_data):
        return True


class SubjectConsentForm(BaseBcppConsentForm):

    def clean(self):
        try:
            obj = StudySpecific.objects.all()[0]
        except IndexError:
            raise forms.ValidationError("Please contact your DATA/IT assistant to add your edc.core.bhp_variables site specifics")
        cleaned_data = self.cleaned_data
        household_member = cleaned_data.get("household_member")
        # Verify that the DOB is not changed in consent after subject is enrolled in HIC
        if HicEnrollment.objects.filter(subject_visit__household_member=household_member).exists():
            hic_enrollment = HicEnrollment.objects.get(subject_visit__household_member=household_member)
            if cleaned_data.get("dob") != hic_enrollment.dob:  # consent_datetime is not editable. So no need to check it here.
                raise forms.ValidationError('An HicEnrollment form already exists for this Subject. So \'dob\' cannot changed.')
        # Verify the data is identical to that entered in the enrollment checklist for BHS
        if EnrolmentChecklist.objects.filter(household_member=household_member).exists():
            enrolment_checklist = EnrolmentChecklist.objects.get(household_member=household_member)
            self.enrollment_checklist_checks(enrolment_checklist, cleaned_data, obj)

        return super(SubjectConsentForm, self).clean()

    class Meta:
        model = SubjectConsent
