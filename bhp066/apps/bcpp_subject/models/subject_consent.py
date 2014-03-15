from django.db import models
from django.core.exceptions import ValidationError

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import YES_NO, YES_NO_NA
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.map.classes import site_mappers
from edc.subject.consent.mixins.bw import IdentityFieldsMixin
from edc.subject.consent.mixins import ReviewAndUnderstandingFieldsMixin


from apps.bcpp.choices import COMMUNITIES

from .base_household_member_consent import BaseHouseholdMemberConsent

from .subject_off_study_mixin import SubjectOffStudyMixin
from .subject_consent_history import SubjectConsentHistory
from .hic_enrollment import HicEnrollment

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
        self.community = self.household_member.household_structure.household.plot.community
        super(BaseSubjectConsent, self).save(*args, **kwargs)

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
        if HicEnrollment.objects.filter(subject_visit__household_member = self.household_member).exists():
            hic_enrollment = HicEnrollment.objects.get(subject_visit__household_member = self.household_member)
            if self.dob != hic_enrollment.dob or self.consent_datetime != hic_enrollment.consent_datetime:
                raise TypeError('An HicEnrollment form already exists for this Subject. So \'dob\' and \'consent_dateitme\' cannot changed.')
        if not (self.citizen or (self.legal_marriage and  self.marriage_certificate)):
            raise TypeError('The subject has to be a citizen, or legally married to a citizen to consent.')
        super(SubjectConsent, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ('subject_identifier', 'survey')


# research blood draw consent
class SubjectConsentRbd(BaseSubjectConsent):

    history = AuditTrail()

    def bypass_for_edit_dispatched_as_item(self):
        return True

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = 'Blood Draw Consent'
        verbose_name_plural = 'Blood Draw Consent'
        unique_together = ('subject_identifier', 'survey')

