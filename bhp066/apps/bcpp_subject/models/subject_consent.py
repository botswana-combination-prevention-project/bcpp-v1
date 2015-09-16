from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import YES_NO, YES_NO_NA
from edc.constants import NOT_APPLICABLE
from edc.map.classes import site_mappers
#from edc.subject.consent.mixins import ReviewAndUnderstandingFieldsMixin
#from edc.subject.consent.mixins.bw import IdentityFieldsMixin
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_consent.models.fields import (ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
                                       SampleCollectionFieldsMixin)
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.core.bhp_variables.models import StudySite

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_household_member.constants import BHS_ELIGIBLE, BHS
from apps.bcpp_household_member.models import EnrollmentChecklist
from apps.bcpp_household_member.exceptions import MemberStatusError

from ..managers import SubjectConsentManager

from .base_household_member_consent import BaseHouseholdMemberConsent
from .hic_enrollment import HicEnrollment
from .subject_consent_history import SubjectConsentHistory
from .subject_off_study_mixin import SubjectOffStudyMixin



# Note below: Mixin fields are added after the abstract class, BaseSubjectConsent, and before
# the concrete class, SubjectConsent, using the field.contribute_to_class method.
# Do it this way so both South and AuditTrail are happy.


# declare abstract base class
class BaseSubjectConsent(SubjectOffStudyMixin, BaseHouseholdMemberConsent):

    study_site = models.ForeignKey(StudySite,
        verbose_name='Site',
        null=True,
        help_text="This refers to the site or 'clinic area' where the subject is being consented."
        )

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
        default=NOT_APPLICABLE,
        help_text="If 'NO' participant will not be enrolled.",
        )

    marriage_certificate = models.CharField(
        verbose_name=("[Interviewer] Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
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
        help_text=('Subject is a minor if aged 16-17. A guardian must be present for consent. '
                   'HIV status may NOT be revealed in the household.'))

    consent_signature = models.CharField(
        verbose_name=("The client has signed the consent form?"),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=False,
        # default='Yes',
        help_text="If no, INELIGIBLE",
        )

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    # see additional mixin fields below

    def save(self, *args, **kwargs):
        if not self.id:
            expected_member_status = BHS_ELIGIBLE
        else:
            expected_member_status = BHS
        if self.household_member.member_status != expected_member_status:
            raise MemberStatusError('Expected member status to be {0}. Got {1} for {2}.'.format(
                expected_member_status, self.household_member.member_status, self.household_member))
        self.is_minor = 'Yes' if self.minor else 'No'
        self.matches_enrollment_checklist(self, self.household_member)
        self.matches_hic_enrollment(self, self.household_member)
        self.community = self.household_member.household_structure.household.plot.community
        super(BaseSubjectConsent, self).save(*args, **kwargs)

    def matches_hic_enrollment(self, subject_consent, household_member, exception_cls=None):
        exception_cls = exception_cls or ValidationError

        if HicEnrollment.objects.filter(subject_visit__household_member=household_member).exists():
            hic_enrollment = HicEnrollment.objects.get(subject_visit__household_member=household_member)
            # consent_datetime does not exist in cleaned_data as it not editable.
            # if subject_consent.dob != hic_enrollment.dob or
            # subject_consent.consent_datetime != hic_enrollment.consent_datetime:
            if subject_consent.dob != hic_enrollment.dob:
                raise exception_cls('An HicEnrollment form already exists for this '
                                    'Subject. So \'dob\' cannot be changed.')

    def matches_enrollment_checklist(self, subject_consent, household_member, exception_cls=None):
        """Matches values in this consent against the enrollment checklist.

        ..note:: the enrollment checklist is required for consent, so always exists."""
        # enrollment checklist is only filled for the same survey as the consent
        household_member = subject_consent.household_member
        exception_cls = exception_cls or ValidationError
        if not EnrollmentChecklist.objects.filter(household_member=household_member).exists():
            raise exception_cls('Enrollment Checklist not found. The Enrollment Checklist is required before consent.')
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        if enrollment_checklist.dob != subject_consent.dob:
            raise exception_cls('Dob does not match that on the enrollment checklist')
        if enrollment_checklist.initials != subject_consent.initials:
            raise exception_cls('Initials do not match those on the enrollment checklist')
        if (enrollment_checklist.guardian.lower() == 'yes' and
                not (subject_consent.minor and subject_consent.guardian_name)):
            raise exception_cls('Enrollment Checklist indicates that subject is a minor with guardian '
                                'available, but the consent does not indicate this.')
        if enrollment_checklist.gender != subject_consent.gender:
            raise exception_cls('Gender does not match that in the enrollment checklist')
        if enrollment_checklist.citizen != subject_consent.citizen:
            raise exception_cls(
                'Answer to whether this subject a citizen, does not match that in enrollment checklist.')
        if (enrollment_checklist.literacy.lower() == 'yes' and
                not (subject_consent.is_literate.lower() == 'yes' or (subject_consent.is_literate.lower() == 'no') and
                     subject_consent.witness_name)):
            raise exception_cls('Answer to whether this subject is literate/not literate but with a '
                                'literate witness, does not match that in enrollment checklist.')
        if ((enrollment_checklist.legal_marriage.lower() == 'yes' and
                enrollment_checklist.marriage_certificate.lower() == 'yes') and not (
                subject_consent.legal_marriage.lower() == 'yes' and
                subject_consent.marriage_certificate.lower() == 'yes')):
            raise exception_cls('Enrollment Checklist indicates that this subject is married '
                                'to a citizen with a valid marriage certificate, but the '
                                'consent does not indicate this.')
        if not household_member.eligible_subject:
            raise exception_cls('Subject is not eligible or has not been confirmed eligible '
                                'for BHS. Perhaps catch this in the forms.py. Got {0}'.format(household_member))
        return True

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

    @property
    def age_at_consent(self):
        age_in_years = relativedelta(date.today(), self.dob).years
        years_since_consent = relativedelta(date.today(), self.consent_datetime).years
        return age_in_years - years_since_consent

    @property
    def survey_of_consent(self):
        return self.survey.survey_name

    @property
    def minor(self):
        age_at_consent = relativedelta(date(self.consent_datetime.year,
                                            self.consent_datetime.month,
                                            self.consent_datetime.day),
                                       self.dob).years
        return age_at_consent >= 16 and age_at_consent <= 17

    class Meta:
        abstract = True

# add Mixin fields to abstract class
# for field in IdentityFieldsMixin._meta.fields:
#     if field.name not in [fld.name for fld in BaseSubjectConsent._meta.fields]:
#         field.contribute_to_class(BaseSubjectConsent, field.name)
# 
# for field in ReviewFieldsMixin._meta.fields:
#     if field.name not in [fld.name for fld in BaseSubjectConsent._meta.fields]:
#         field.contribute_to_class(BaseSubjectConsent, field.name)


# declare concrete class
class SubjectConsent(IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin, SampleCollectionFieldsMixin,
                     VulnerabilityFieldsMixin, BaseSubjectConsent):

    history = AuditTrail()

    objects = SubjectConsentManager()

    def dispatch_container_lookup(self, using=None):
        return (models.get_model('bcpp_household', 'Plot'),
                'household_member__household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = (('subject_identifier', 'survey', 'version'), ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )
