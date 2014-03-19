from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import YES_NO, YES_NO_NA
from edc.map.classes import site_mappers
from edc.subject.consent.mixins import ReviewAndUnderstandingFieldsMixin
from edc.subject.consent.mixins.bw import IdentityFieldsMixin
from edc.subject.lab_tracker.classes import site_lab_tracker

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_household_member.models import EnrolmentChecklist

from .base_household_member_consent import BaseHouseholdMemberConsent
from .hic_enrollment import HicEnrollment
from .subject_consent_history import SubjectConsentHistory
from .subject_off_study_mixin import SubjectOffStudyMixin

# Note below: Mixin fields are added after the abstract class, BaseSubjectConsent, and before
# the concrete class, SubjectConsent, using the field.contribute_to_class method.
# Do it this way so both South and AuditTrail are happy.


# declare abstract base class
class BaseSubjectConsent(SubjectOffStudyMixin, BaseHouseholdMemberConsent):

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
        help_text="",
        )

    legal_marriage = models.CharField(
        verbose_name=("If not a citizen, are you legally married to a Botswana Citizen?"),
        max_length=3,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default='N/A',
        help_text="If 'NO' participant will not be enrolled.",
        )

    marriage_certificate = models.CharField(
        verbose_name=("[Interviewer] Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default='N/A',
        help_text="If 'NO' participant will not be enrolled.",
        )

    marriage_certificate_no = models.CharField(
        verbose_name=("What is the marriage certificate number?"),
        max_length=9,
        null=True,
        blank=True,
        help_text="e.g. 000/YYYY",
        )

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text='Subject is a minor if aged 16-17. A guardian must be present for consent. HIV status may NOT be revealed in the household.')

    consent_signature = models.CharField(
        verbose_name=("The client has signed the consent form?"),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=False,
        #default='Yes',
        help_text="If no, INELIGIBLE",
        )

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    # see additional mixin fields below

    def save(self, *args, **kwargs):
        self.is_minor = self.get_is_minor()
        self.matches_enrollment_checklist()
        self.community = self.household_member.household_structure.household.plot.community
        self.enroll_household()
        self.household_member.is_consented = True
        self.household_member.save()
        super(BaseSubjectConsent, self).save(*args, **kwargs)

    def matches_enrollment_checklist(self, exception_cls=None):
        """Matches values in this consent against the enrolmnet checklist.

        ..note:: the enrollment checklist is required for consent, so always exists."""
        exception_cls = exception_cls or ValidationError
        enrollment_checklist = self.get_enrollment_checklist_query_set()
        if enrollment_checklist.count() != 1:
            raise exception_cls('There should be 1 enrollment checklist for individual prior to consenting. Got {0}'.format(enrollment_checklist.count()))
        else:
            enrollment_checklist = enrollment_checklist[0]
        if enrollment_checklist.dob != self.dob:
            raise exception_cls('Dob does not match that on the enrollment checklist')
        if enrollment_checklist.initials != self.initials:
            raise exception_cls('Initials do not match those on the enrollment checklist')
        if enrollment_checklist.guardian.lower() == 'yes' and not (self.is_minor.lower() == 'yes' and self.guardian_name):
            raise exception_cls('Enrollment checklist indicates that subject is a minor with guardian available, but the consent does not indicate this.')
        if enrollment_checklist.gender != self.gender:
            raise exception_cls('Gender does not match that in the enrollment checklist')
        if enrollment_checklist.citizen != self.citizen:
            raise exception_cls('Enrollment checklist indicates that this subject is a citizen, but the consent does not indicate this.')
        if ((enrollment_checklist.legal_marriage.lower() == 'yes' and enrollment_checklist.marriage_certificate.lower() == 'yes') and
                not (self.legal_marriage.lower() == 'yes' and self.marriage_certificate.lower() == 'yes')):
            raise exception_cls('Enrollment checklist indicates that this subject is married to a citizen with a valid marriage certificate, but the consent does not indicate this.')
        if not self.household_member.eligible_subject:
            raise exception_cls('Subject is not eligible or has not been confirmed eligible for BHS. Perhaps catch this in the forms.py. Got {0}'.format(self.household_member))
        return True

    def enroll_household(self):
        """Updates the household structure as enrolled if the member consents.

        ..note:: household structure will update the household as enrolled."""
        # household_structure is enrolled if a member consents
        household_structure = self.household_member.household_structure
        if not household_structure.enrolled:
            household_structure.enrolled = True
            household_structure.enrolled_datetime = datetime.today()
            household_structure.save()

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    def get_subject_type(self):
        return 'subject'

    def get_consent_history_model(self):
        return SubjectConsentHistory

    def get_registered_subject(self):
        return self.registered_subject

    def get_hiv_status(self):
        """Returns the hiv testing history as a string.

        .. note:: more than one table is tracked so the history includes HIV results not performed by our team
                  as well as the results of tests we perform."""
        return site_lab_tracker.get_history_as_string('HIV', self.subject_identifier, 'subject')

    def get_is_minor(self):
        if self.age == 16 or self.age == 17:
            return 'Yes'
        return 'No'

    @property
    def age(self):
        return relativedelta(date.today(), self.dob).years

    class Meta:
        abstract = True

# add Mixin fields to abstract class
for field in IdentityFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseSubjectConsent._meta.fields]:
        field.contribute_to_class(BaseSubjectConsent, field.name)

for field in ReviewAndUnderstandingFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseSubjectConsent._meta.fields]:
        field.contribute_to_class(BaseSubjectConsent, field.name)


# declare concrete class
class SubjectConsent(BaseSubjectConsent):

    history = AuditTrail()

    def bypass_for_edit_dispatched_as_item(self):
        return True

    def save(self, *args, **kwargs):
        self.matches_hic_enrollment_values()
        super(SubjectConsent, self).save(*args, **kwargs)

    def matches_hic_enrollment_values(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if HicEnrollment.objects.filter(subject_visit__household_member=self.household_member).exists():
            hic_enrollment = HicEnrollment.objects.get(subject_visit__household_member=self.household_member)
            if self.dob != hic_enrollment.dob or self.consent_datetime != hic_enrollment.consent_datetime:
                raise exception_cls('An HicEnrollment form already exists for this Subject. So \'dob\' and \'consent_dateitme\' cannot changed.')
        if not (self.citizen or (self.legal_marriage and  self.marriage_certificate)):
            raise exception_cls('The subject has to be a citizen, or legally married to a citizen to consent.')

    def get_enrollment_checklist_query_set(self):
        #For every consented individual there has to be an enrollment checklist. Its enforced.
        return EnrolmentChecklist.objects.filter(household_member=self.household_member)

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ('subject_identifier', 'survey')
