from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import dob_not_future
from edc.choices.common import YES_NO_UNKNOWN, GENDER, YES_NO_NA, YES_NO
from edc.constants import NOT_APPLICABLE
from edc.core.crypto_fields.fields import EncryptedFirstnameField
from edc.subject.registration.models import RegisteredSubject

from .base_clinic_registered_subject_model import BaseClinicRegisteredSubjectModel

from apps.clinic.choices import VERBALHIVRESULT_CHOICE, INABILITY_TO_PARTICIPATE_REASON


class ClinicEligibility (BaseClinicRegisteredSubjectModel):

    first_name = EncryptedFirstnameField(
        verbose_name='First name',
        validators=[RegexValidator("^[A-Z]{1,250}$", "Ensure first name is only CAPS and does not contain any spaces or numbers")],
        db_index=True)

    initials = models.CharField('Initials',
        max_length=3,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3),
            RegexValidator("^[A-Z]{1,3}$", "Must be Only CAPS and 2 or 3 letters. No spaces or numbers allowed.")],
        db_index=True)

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER,
        db_index=True)

    dob = models.DateField(
        verbose_name=_("Date of birth"),
        validators=[
            dob_not_future,
#             MinConsentAge,
#             MaxConsentAge,
            ],
        help_text="Format is YYYY-MM-DD",
        )

    has_identity = models.CharField(
        verbose_name=_("[Interviewer] Has the subject presented a valid OMANG or other identity document?"),
        max_length=10,
        choices=YES_NO,
        help_text=_("Allow Omang, Passport number, driver's license number or Omang receipt number. If 'NO' participant will not be enrolled."))

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
        help_text="")

    legal_marriage = models.CharField(
        verbose_name=_("If not a citizen, are you legally married to a Botswana Citizen?"),
        max_length=3,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        help_text=_("If 'NO' participant will not be enrolled."))

    marriage_certificate = models.CharField(
        verbose_name=("[Interviewer] Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        help_text="If 'NO' participant will not be enrolled.")

    part_time_resident = models.CharField(
        verbose_name=_("In the past 12 months, have you typically spent 3 or"
                      " more nights per month in this community? "),
        max_length=25,
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=False,
        help_text=("If participant has moved into the "
                  "community in the past 12 months, then "
                  "since moving in has the participant typically "
                  "spent more than 3 nights per month in this community. "
                  "If 'NO (or don't want to answer)' STOP. Participant cannot be enrolled."),
        )

    literacy = models.CharField(
        verbose_name=_("Is the participant LITERATE?, or if ILLITERATE, is there a"
                       "  LITERATE witness available "),
        max_length=10,
        choices=YES_NO,
        help_text=_("If participate is illiterate, confirm there is a literate"
                    "witness available otherwise participant will not be enrolled."))

    inability_to_participate = models.CharField(
        verbose_name=_("Does any of the following reasons apply to the participant?(Any of this reasons makes the participant unable to take part in the informed consent process)"),
        max_length=17,
        choices=INABILITY_TO_PARTICIPATE_REASON,
        null=True,
        blank=False,
        help_text=("Participant can only participate if NONE is selected."),
        )

    hiv_status = models.CharField(
        verbose_name=_("Please tell me your current HIV status?"),
        max_length=30,
        null=True,
        blank=True,
        choices=VERBALHIVRESULT_CHOICE,
        )

    is_eligible = models.BooleanField(default=False)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.is_eligible = False
        self.match_consent_values(self)
        if self.eligible_clinic_subject():
            self.is_eligible = True
        super(ClinicEligibility, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} ({}) -{}- (DOB:{})".format(self.first_name, self.initials, self.gender, self.dob)

    def get_registration_datetime(self):
        return self.registration_datetime

    def eligible_clinic_subject(self):
        age_in_years = relativedelta(date.today(), self.dob).years
        return (self.hiv_status == 'POS' and self.part_time_resident == 'Yes' and self.legal_marriage != 'No'
                and age_in_years >= 16 and age_in_years <= 64 and self.inability_to_participate == 'None')

    def match_consent_values(self, eligibility_checklist, exception_cls=None):
        error_msg = None
        exception_cls = exception_cls or ValidationError
        from apps.bcpp_clinic.models import ClinicConsent
        consent = ClinicConsent.objects.filter(registered_subject__registration_identifier=self.id)
        if consent.exists():
            consent = consent[0]
            if  eligibility_checklist.dob != consent.dob:
                error_msg = "The DoB does not match that entered in the consent. {0} <> {1}".format(eligibility_checklist.dob, consent.dob)
            if  eligibility_checklist.first_name != consent.first_name:
                error_msg = "The first name does not match that entered in the consent. {0} <> {1}".format(eligibility_checklist.first_name, consent.first_name)
            if  eligibility_checklist.initials != consent.initials:
                error_msg = "The initials do not match those entered in the consent. {0} <> {1}".format(eligibility_checklist.initials, consent.initials)
            if  eligibility_checklist.gender != consent.gender:
                error_msg = "The gender does not match that entered in the consent. {0} <> {1}".format(eligibility_checklist.gender, consent.gender)
            if error_msg:
                raise exception_cls(error_msg)
        return True

    def get_consent(self):
        clinic_consent = models.get_model('bcpp_clinic', 'clinicconsent')
        if clinic_consent.objects.filter(registered_subject__registration_identifier=self.id).exists():
            return clinic_consent.objects.filter(registered_subject__registration_identifier=self.id)[0]
        return None

    def update_registered_subject_on_post_save(self, **kwargs):
        using = kwargs.get('using', None)
        # decide now, either access an existing registered_subject or create a new one
        if RegisteredSubject.objects.using(using).filter(registration_identifier=self.id).exists():
            registered_subject = RegisteredSubject.objects.using(using).get(registration_identifier=self.id)
        else:
            # define registered_subject now as the audit trail requires access to the registered_subject object
            # even if no subject_identifier exists. That is, it is going to call
            # get_subject_identifier().
            registered_subject = RegisteredSubject.objects.using(using).create(
                created=self.created,
                first_name=self.first_name,
                initials=self.initials,
                dob=self.dob,
                gender=self.gender,
                subject_type='subject',
                subject_identifier_as_pk=self.id,
                registration_identifier=self.id,
                registration_datetime=self.created,
                user_created=self.user_created,
                registration_status='member',)
            # set registered_subject for this hsm
            self.registered_subject = registered_subject
            print RegisteredSubject.objects.all().count()
            self.save(using=using)

    def delete_enrollment_loss(self, **kwargs):
        """Deletes a clinic enrollment loss based if a clinic eligibility checklist is now passed."""
        from ..models import ClinicEnrollmentLoss
        clinic_loss = ClinicEnrollmentLoss.objects.filter(registered_subject=self.registered_subject)
        if clinic_loss.exists():
            clinic_loss[0].delete()

    def create_enrollment_loss(self, **kwargs):
        """Creates or updates the clinic enrollment loss based on the reason for not passing the clinic eligibility checklist."""
        from ..models import ClinicEnrollmentLoss
        reason = []
        age_in_years = relativedelta(date.today(), self.dob).years
        if not (age_in_years >= 16 and age_in_years <= 64):
            reason.append('Must be aged between >=16 and <=64 years.')
        if self.part_time_resident != 'Yes':
            reason.append('Does not spend 3 or more nights per month in the community.')
        if self.legal_marriage == 'No':
            reason.append('Not a citizen and not married to a citizen.')
        if self.inability_to_participate != 'None':
            reason.append('Mental Incapacity/Deaf/Mute/Too sick.')
        if self.hiv_status != 'POS':
            reason.append('HIV status is not Positive.')
        if reason:
            clinic_loss = ClinicEnrollmentLoss.objects.filter(registered_subject=self.registered_subject)
            if clinic_loss.exists():
                clinic_loss = clinic_loss[0]
                clinic_loss.registration_datetime = datetime.today()
                clinic_loss.reason = '; '.join(reason)
                clinic_loss.save()
            else:
                ClinicEnrollmentLoss.objects.create(
                    registered_subject=self.registered_subject,
                    registration_datetime=datetime.today(),
                    reason=';'.join(reason))
        return reason

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Eligibility"
        verbose_name_plural = "Clinic Eligibility"
