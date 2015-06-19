from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import YES_NO, YES_NO_NA, YES_NO_UNKNOWN
from edc.constants import NOT_APPLICABLE
from edc.map.classes import site_mappers
from edc.subject.consent.mixins import ReviewAndUnderstandingFieldsMixin
from edc.subject.consent.mixins.bw import IdentityFieldsMixin

from .base_household_member_consent import BaseHouseholdMemberConsent
from .clinic_consent_history import ClinicConsentHistory
from .clinic_off_study_mixin import ClinicOffStudyMixin


class BaseClinicConsent(ClinicOffStudyMixin, BaseHouseholdMemberConsent):

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
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
        help_text="If no, INELIGIBLE",
        )

    community = models.CharField(max_length=25, editable=False)

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    def get_subject_type(self):
        return 'subject'

    def get_consent_history_model(self):
        return ClinicConsentHistory

    def get_registered_subject(self):
        return self.registered_subject

    def is_dispatchable_model(self):
        return False

    class Meta:
        abstract = True

# add Mixin fields to abstract class
for field in IdentityFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseClinicConsent._meta.fields]:
        field.contribute_to_class(BaseClinicConsent, field.name)

for field in ReviewAndUnderstandingFieldsMixin._meta.fields:
    if field.name not in [fld.name for fld in BaseClinicConsent._meta.fields]:
        field.contribute_to_class(BaseClinicConsent, field.name)


# declare concrete class
class ClinicConsent(BaseClinicConsent):
    """A model completed by the user to capture the ICF."""
    lab_identifier = models.CharField(
        verbose_name=("lab allocated identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
        )

    htc_identifier = models.CharField(
        verbose_name=("HTC Identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
        )

    pims_identifier = models.CharField(
        verbose_name=("PIMS identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text="if known."
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.community = site_mappers.get_current_mapper().map_area
        super(ClinicConsent, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Consent RBD'
        verbose_name_plural = 'Clinic Consent RBD'
