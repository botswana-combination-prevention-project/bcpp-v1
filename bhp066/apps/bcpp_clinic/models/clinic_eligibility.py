from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import dob_not_future
from edc.base.model.fields import IdentityTypeField
from edc.base.model.fields.local.bw import EncryptedOmangField
from edc.base.model.validators import (datetime_not_before_study_start, datetime_not_future,
                                       MinConsentAge, MaxConsentAge)
from edc.choices.common import YES_NO_UNKNOWN, GENDER, YES_NO_NA, YES_NO
from edc.constants import NOT_APPLICABLE
from edc.core.crypto_fields.fields import EncryptedFirstnameField
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.map.classes import site_mappers
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp.choices import INABILITY_TO_PARTICIPATE_REASON, VERBALHIVRESULT_CHOICE
from apps.bcpp_clinic.models.clinic_refusal import ClinicRefusal
from apps.bcpp_household_member.constants import CLINIC_RBD
from apps.bcpp_household_member.models import HouseholdMember

from apps.bcpp_subject.models import SubjectConsent

from ..managers import BaseClinicHouseholdMemberManager

from .clinic_consent import ClinicConsent
from .clinic_enrollment_loss import ClinicEnrollmentLoss
from .clinic_household_member import ClinicHouseholdMember


class ClinicEligibility (BaseDispatchSyncUuidModel):
    """A model completed by the user that confirms and saves eligibility
    information for potential participant."""

    household_member = models.OneToOneField(HouseholdMember,
        null=True,
        blank=True,
        help_text='Created automatically and associated with the clinic plot.'
        )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
            ],
        help_text='Date and time of collection'
        )

    first_name = EncryptedFirstnameField(
        verbose_name='First name',
        validators=[RegexValidator("^[A-Z]{1,250}$", "Ensure first name is in CAPS and "
                                   "does not contain any spaces or numbers")],
        help_text="")

    initials = models.CharField(
        verbose_name='Initials',
        max_length=3,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3),
            RegexValidator("^[A-Z]{1,3}$", "Must be Only CAPS and 2 or 3 letters. No spaces or numbers allowed.")],
        help_text="")

    dob = models.DateField(
        verbose_name="Date of birth",
        validators=[dob_not_future, ],
        null=True,
        blank=True,
        help_text="Format is YYYY-MM-DD.")

    verbal_age = models.IntegerField(
        verbose_name='Age in years as reported by patient',
        null=True,
        blank=True,
        help_text='Complete if DOB is not provided, otherwise leave BLANK.')

    guardian = models.CharField(
        verbose_name=_("If minor, is there a guardian available? "),
        max_length=10,
        choices=YES_NO_NA,
        help_text=_("If a minor age 16 and 17, ensure a guardian is available otherwise"
                    " participant will not be enrolled."))

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER)

    has_identity = models.CharField(
        verbose_name=_("[Interviewer] Has the subject presented a valid OMANG or other identity document?"),
        max_length=10,
        choices=YES_NO,
        help_text=_('Allow Omang, Passport number, driver\'s license number or Omang receipt number. '
                    'If \'NO\' participant will not be enrolled.'))

    identity = EncryptedOmangField(
        verbose_name=_("Identity number (OMANG, etc)"),
        unique=True,
        null=True,
        blank=True,
        help_text=("Use Omang, Passport number, driver's license number or Omang receipt number")
        )

    identity_type = IdentityTypeField(
        null=True)

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text="")

    legal_marriage = models.CharField(
        verbose_name=_("If not a citizen, are you legally married to a Botswana Citizen?"),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=_("If 'NO' participant is not eligible."))

    marriage_certificate = models.CharField(
        verbose_name=("[Interviewer] Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If 'NO' participant is not eligible.")

    part_time_resident = models.CharField(
        verbose_name=_("In the past 12 months, have you typically spent 3 or"
                       " more nights per month in this community? "),
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text=(
            "If participant has moved into the "
            "community in the past 12 months, then "
            "since moving in has the participant typically "
            "spent more than 3 nights per month in this community. "
            "If 'NO (or don't want to answer)' STOP. Participant is not eligible."),
        )

    literacy = models.CharField(
        verbose_name=_("Is the participant LITERATE?, or if ILLITERATE, is there a"
                       "  LITERATE witness available "),
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text=_("If participate is illiterate, confirm there is a literate"
                    "witness available otherwise participant is not eligible."))

    inability_to_participate = models.CharField(
        verbose_name=_("Do any of the following reasons apply to the participant?"),
        max_length=17,
        choices=INABILITY_TO_PARTICIPATE_REASON,
        help_text=("Participant can only participate if NONE is selected. "
                   "(Any of these reasons make the participant unable to take "
                   "part in the informed consent process)"),
        )

    hiv_status = models.CharField(
        verbose_name=_("Please tell me your current HIV status?"),
        max_length=30,
        choices=VERBALHIVRESULT_CHOICE,
        help_text='If not HIV(+) participant is not elgiible.'
        )

    age_in_years = models.IntegerField(editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    is_consented = models.BooleanField(
        default=False,
        editable=False)

    is_refused = models.BooleanField(
        default=False,
        editable=False)

    loss_reason = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        null=True,
        editable=False,
        help_text='(stored for the loss form)')

    community = models.CharField(max_length=25, editable=False)

    history = AuditTrail()

    objects = BaseClinicHouseholdMemberManager()

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        if update_fields == ['is_consented'] or update_fields == ['is_refused']:
            pass
        else:
            if not self.id:
                try:
                    registered_subject = RegisteredSubject.objects.get(identity=self.identity)
                    raise ValueError('A subject with this OMANG is alreay registered. See {}. '
                                     'Perhaps catch this on the form'.format(registered_subject))
                except RegisteredSubject.DoesNotExist:
                    pass
            self.age_in_years = relativedelta(self.report_datetime.date(), self.dob).years
            self.household_member = self.clinic_household_member
            self.is_eligible, self.loss_reason = self.passes_enrollment_criteria()
            self.consented()  # checks if consented already
            self.community = site_mappers.get_current_mapper().map_area
        super(ClinicEligibility, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} ({}) {}/{}".format(self.first_name, self.initials, self.gender, self.age_in_years)

    def natural_key(self):
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.householdmember', ]

    def get_registered_subject(self):
        return self.household_member.register_subject

    @property
    def clinic_household_member(self):
        """Returns the household_member and will create if one does not exist."""
        try:
            pk = self.household_member.pk
        except AttributeError:
            pk = None
        try:
            clinic_household_member = ClinicHouseholdMember.objects.get(pk=pk)
            clinic_household_member.first_name = self.first_name
            clinic_household_member.initials = self.initials
            clinic_household_member.age_in_years = self.age_in_years
            clinic_household_member.gender = self.gender
            clinic_household_member.save()
        except ClinicHouseholdMember.DoesNotExist:
            clinic_household_member = ClinicHouseholdMember.objects.create(
                first_name=self.first_name,
                initials=self.initials,
                age_in_years=self.age_in_years,
                gender=self.gender,
                present_today='N/A',
                inability_to_participate=self.inability_to_participate,
                study_resident=self.part_time_resident,
                member_status=CLINIC_RBD,
                is_consented=False,
                relation='UNKNOWN',
                eligible_member=True,
                eligible_subject=True,
                )
        return clinic_household_member

    def consented(self, exception_cls=None):
        """Confirms subject has not previously consented with this personal identifier."""
        exception_cls = exception_cls or ValidationError
        clinic_consent = None
        try:
            clinic_consent = ClinicConsent.objects.get(household_member=self.household_member)
            raise exception_cls('Household member {} was consented as {} on {}. '
                                'Eligibility checklist may not be edited.'.format(
                                    self.household_member,
                                    clinic_consent.subject_identifier,
                                    clinic_consent.consent_datetime))
        except ClinicConsent.DoesNotExist:
            pass
        try:
            subject_consent = SubjectConsent.objects.get(identity=self.identity)
            raise exception_cls('A Household member was consented during BHS with study identifier {} on {}. '
                                'Eligibility checklist may not be completed for personal identifier {}.'.format(
                                    subject_consent.subject_identifier,
                                    subject_consent.modified,
                                    subject_consent.identity))
        except SubjectConsent.DoesNotExist:
            pass
        return None

    def passes_enrollment_criteria(self):
        """Creates or updates (or deletes) the enrollment loss based on the
        reason for not passing the enrollment checklist."""
        loss_reason = []
        if self.age_in_years < 16:
            loss_reason.append('Too young (<16).')
        if self.age_in_years > 64:
            loss_reason.append('Too old (>64).')
        if self.has_identity == 'No' or not self.identity:
            loss_reason.append('No valid identity.')
        if self.part_time_resident == 'No':
            loss_reason.append('Not resident.')
        if self.part_time_resident == 'Unknown':
            loss_reason.append('Residency unknown.')
        if self.citizen == 'No' and self.legal_marriage == 'No':
            loss_reason.append('Not a citizen and not married to a citizen.')
        if (self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'yes' and
                self.marriage_certificate == 'No'):
            loss_reason.append('Not a citizen, married to a citizen but does not have a marriage certificate.')
        if self.literacy == 'No':
            loss_reason.append('Illiterate with no literate witness.')
        if self.literacy == 'Unknown':
            loss_reason.append('Literacy unknown.')
        if self.household_member.is_minor and self.guardian != 'Yes':
            loss_reason.append('Minor without guardian available.')
        if self.inability_to_participate != 'N/A':
            loss_reason.append('Mental Incapacity/Deaf/Mute/Too sick.')
        if self.hiv_status == 'NEG':
            loss_reason.append('HIV Negative.')
        if self.hiv_status != 'POS' and self.hiv_status != 'NEG':
            loss_reason.append('HIV status unknown.')
        if not self.identity:
            loss_reason.append('Identity unknown.')
        if not self.dob:
            loss_reason.append('DOB unknown.')
        if not self.citizen:
            loss_reason.append('Citizenship unknown.')
        return (False if loss_reason else True, loss_reason)

    @property
    def reason_ineligible(self):
        reason = []
        if self.age_in_years < 16:
            reason.append('Minor.')
        if self.age_in_years > 64:
            reason.append('Too old.')
        if self.part_time_resident == 'No':
            reason.append('Not resident.')
        if self.part_time_resident == 'Unknown':
            reason.append('Residency unknown.')
        if self.legal_marriage == 'No':
            reason.append('Not a citizen and not married to a citizen.')
        if self.inability_to_participate:
            reason.append('Mental Incapacity/Deaf/Mute/Too sick.')
        if self.hiv_status == 'NEG':
            reason.append('HIV Negative.')
        if self.hiv_status != 'POS' and self.hiv_status != 'NEG':
            reason.append('HIV status unknown.')
        if not self.identity:
            reason.append('Identity unknown.')
        if not self.dob:
            reason.append('DOB unknown.')
        if not self.citizen:
            reason.append('Citizenship unknown.')
        reason.sort()
        return '; '.join(reason)

    @property
    def clinic_refusal(self):
        try:
            clinic_refusal = ClinicRefusal.objects.get(household_member=self.household_member)
        except ClinicRefusal.DoesNotExist:
            clinic_refusal = None
        return clinic_refusal

    @property
    def clinic_consent(self):
        try:
            clinic_consent = ClinicConsent.objects.get(household_member=self.household_member)
        except ClinicRefusal.DoesNotExist:
            clinic_consent = None
        return clinic_consent

    @property
    def clinic_enrollment_loss(self):
        try:
            clinic_enrollment_loss = ClinicEnrollmentLoss.objects.get(household_member=self.household_member)
        except ClinicEnrollmentLoss.DoesNotExist:
            clinic_enrollment_loss = None
        return clinic_enrollment_loss

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Eligibility"
        verbose_name_plural = "Clinic Eligibility"
        unique_together = ['first_name', 'initials']
