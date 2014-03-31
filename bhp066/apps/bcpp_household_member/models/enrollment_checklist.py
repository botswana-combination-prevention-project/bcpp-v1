from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models

from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc.choices.common import GENDER
from edc.choices.common import YES_NO, YES_NO_NA
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..constants import BHS_SCREEN, BHS_ELIGIBLE
from ..exceptions import MemberStatusError
from ..managers import EnrollmentChecklistManager

from .enrollment_loss import EnrollmentLoss
from .household_member import HouseholdMember


class EnrollmentChecklist(BaseDispatchSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember)

    initials = models.CharField('Initials',
        max_length=3,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3),
            RegexValidator("^[A-Z]{1,3}$", "Must be Only CAPS and 2 or 3 letters. No spaces or numbers allowed.")],
        db_index=True)

    dob = models.DateField(
        verbose_name="Date of birth",
        validators=[
            dob_not_future,
            MinConsentAge,
            MaxConsentAge,
            ],
        null=True,
        blank=False,
        help_text="Format is YYYY-MM-DD. (Data will not be saved)",
        )

    guardian = models.CharField(
        verbose_name=("If minor, is there a guardian available? "),
        max_length=10,
        choices=YES_NO_NA,
        help_text=("If a minor age 16 and 17, ensure a guardian is available otherwise"
                   " participant will not be enrolled."),
        )

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER,
        max_length=1,
        null=True,
        blank=False,
        )

    has_identity = models.CharField(
        verbose_name="[Interviewer] Has the subject presented a valid OMANG or other identity document?",
        max_length=10,
        choices=YES_NO,
        help_text="Allow Omang, Passport number, driver's license number or Omang receipt number. If 'NO' participant will not be enrolled."
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

    # same as study_resident in household member
    part_time_resident = models.CharField(
        verbose_name=("In the past 12 months, have you typically spent 3 or"
                      " more nights per month in this community? "),
        max_length=10,
        choices=YES_NO,
        help_text=("If participant has moved into the "
                  "community in the past 12 months, then "
                  "since moving in has the participant typically "
                  "spent more than 3 nights per month in this community. "
                  "If 'NO (or don't want to answer)'. Participant will not be enrolled."),
        )

    household_residency = models.CharField(
        verbose_name='In the past 12 months, have you typically spent more nights on average in this household than in any other household in the same community?',
        max_length=3,
        choices=YES_NO,
        help_text="If 'NO' participant will not be enrolled.",
        )

    literacy = models.CharField(
        verbose_name=("Is the participant LITERATE?, or if ILLITERATE, is there a"
                      "  LITERATE witness available "),
        max_length=10,
        choices=YES_NO,
        help_text=("If participate is illiterate, confirm there is a literate"
                   "witness available otherwise participant will not be enrolled."),
        )

    is_eligible = models.BooleanField(default=False)

    objects = EnrollmentChecklistManager()

    def __unicode__(self):
        return str(self.household_member)

    def natural_key(self):
        if not self.household_member:
            raise AttributeError("household_member cannot be None for household_head_eligibility with pk='\{0}\'".format(self.pk))
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household.household_member']

    def dispatch_container_lookup(self, using=None):
        return (models.get_model('bcpp_household', 'Plot'), 'household_member__household_structure__household__plot__plot_identifier')

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.household_member.member_status != BHS_SCREEN:
                raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(BHS_SCREEN, self.household_member.member_status))
        else:
            if self.household_member.member_status not in [BHS_ELIGIBLE, BHS_SCREEN]:
                raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(BHS_SCREEN, self.household_member.member_status))
        self.is_eligible = False
        if self.matches_household_member_values(self, self.household_member):
            if not self.enrollment_loss():
                self.is_eligible = True
        self.household_member.eligible_subject = self.is_eligible
        self.household_member.enrollment_checklist_completed = True
        self.household_member.save()
        super(EnrollmentChecklist, self).save(*args, **kwargs)

    def matches_household_member_values(self, enrollment_checklist, household_member, exception_cls=None):
        """Compares shared values on household_member form and returns True if all match."""
        error_msg = None
        exception_cls = exception_cls or ValidationError
        age_in_years = relativedelta(date.today(), enrollment_checklist.dob).years
        if age_in_years != household_member.age_in_years:
            error_msg = 'Age does not match that entered on the household member. Got {0} <> {1}'.format(age_in_years, household_member.age_in_years)
        elif household_member.study_resident.lower() != enrollment_checklist.part_time_resident.lower():
            error_msg = 'Residency does not match that entered on the household member. Got {0} <> {1}'.format(enrollment_checklist.part_time_resident, household_member.study_resident)
        elif household_member.initials.lower() != enrollment_checklist.initials.lower():
            error_msg = 'Initials do not match those entered on the household member. Got {0} <> {1}'.format(enrollment_checklist.initials, household_member.initials)
        elif household_member.gender != enrollment_checklist.gender:
            error_msg = 'Gender does not match that entered on the household member. Got {0} <> {1}'.format(enrollment_checklist.gender, household_member.gender)
        elif household_member.is_minor and age_in_years >= 18:
            error_msg = 'Member is a minor. Got age {0}'.format(age_in_years)
        if error_msg:
            raise exception_cls(error_msg)
        return True

    def enrollment_loss(self):
        """Creates or updates (or deletes) the enrollment loss based on the reason for noot passing the enrollment checklist."""
        reason = []
        age_in_years = relativedelta(date.today(), self.dob).years
        if not (age_in_years >= 16 and age_in_years <= 64):
            reason.append('Must be aged between >=16 and <=64 years.')
        if self.has_identity.lower() == 'no':
            reason.append('No valid identity.')
        if self.part_time_resident.lower() != 'yes':
            reason.append('Does not spend 3 or more nights per month in the community.')
        if self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'no':
            reason.append('Not a citizen and not married to a citizen.')
        if self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'yes' and self.marriage_certificate.lower() == 'no':
            reason.append('Not a citizen, married to a citizen but does not have a marriage certificate.')
        if self.literacy.lower() == 'no':
            reason.append('Illiterate with no literate witness.')
        if self.household_member.is_minor and self.guardian.lower() != 'yes':
            reason.append('Minor without guardian available.')
        if reason:
            if EnrollmentLoss.objects.filter(household_member=self.household_member):
                enrollment_loss = EnrollmentLoss.objects.get(household_member=self.household_member)
                enrollment_loss.report_datetime = datetime.today()
                enrollment_loss.reason = reason
            else:
                EnrollmentLoss.objects.create(
                    household_member=self.household_member,
                    report_datetime=datetime.today(),
                    reason=';'.join(reason))
        else:
            EnrollmentLoss.objects.filter(household_member=self.household_member).delete()
        return reason

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Enrollment Checklist"
