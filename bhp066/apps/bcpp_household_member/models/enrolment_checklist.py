from datetime import datetime
from dateutils import relativedelta

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc.choices.common import GENDER
from edc.choices.common import YES_NO, YES_NO_DWTA, YES_NO_NA
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from .household_member import HouseholdMember
from .loss import Loss


class EnrolmentChecklist (BaseDispatchSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember)

    initials = models.CharField('Initials',
        max_length=3,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3),
            RegexValidator("^[A-Za-z]{1,3}$", "Must be 2 or 3 letters. No spaces or numbers allowed.")],
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
        choices=YES_NO_DWTA,
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
        verbose_name=("Is the participant LITERATE?, or if ILLITRATE, is there a"
                      "  LITERATE witness available "),
        max_length=10,
        choices=YES_NO,
        help_text=("If participate is illitrate, confirm there is a literate"
                   "witness available otherwise participant will not be enrolled."),
        )

    is_eligible = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.household_member.eligible_subject = False
        age_in_years = relativedelta(datetime.today(), datetime(self.dob.year, self.dob.month, self.dob.day)).years
        if self.matches_household_member_values(age_in_years):
            if not self.has_loss_reason(age_in_years):
                self.household_member.eligible_subject = True
        self.is_eligible = self.household_member.eligible_subject
        self.household_member.eligibility_checklist_filled = True
        self.household_member.save()
        super(EnrolmentChecklist, self).save(*args, **kwargs)

    def matches_household_member_values(self, age_in_years, exception_cls=None):
        """Compares shared values on household_member form and returns True if all match."""
        validation_error = None
        exception_cls = exception_cls or ValidationError
        if age_in_years != self.household_member.age_in_years:
            validation_error = 'Age does not match with that entered on the household member. Got {0} <> {1}'.format(age_in_years, self.household_member.age_in_years)
        if self.household_member.study_resident.lower() != self.part_time_resident.lower():
            validation_error = 'Residency does not with match that entered on the household member. Got {0} <> {1}'.format(self.part_time_resident, self.household_member.study_resident)
        if self.household_member.initials.lower() != self.initials.lower():
            validation_error = 'Initials do not with match that entered on the household member. Got {0} <> {1}'.format(self.initials, self.household_member.initials)
        if validation_error:
            raise exception_cls(validation_error)
        return True

    def has_loss_reason(self, age_in_years):
        """Adds any reasons for ineligibilty to a loss reason list and create a loss model instance."""
        loss_reason = []
        if not (age_in_years >= 16 and age_in_years <= 64):
            loss_reason.append('Must be aged between >=16 and <=64 years.')
        if self.has_identity.lower() == 'no':
            loss_reason.append('No valid identity.')
        if self.part_time_resident.lower() != 'yes':
            loss_reason.append('Does not spend 3 or more nights per month in the community.')
        if self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'no':
            loss_reason.append('Not a citizen and not married to a citizen.')
        if self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'yes' and self.marriage_certificate.lower() == 'no':
            loss_reason.append('Not a citizen, married to a citizen but does not have a marriage certificate.')
        if self.literacy.lower() == 'no':
            loss_reason.append('Illiterate with no literate witness.')
        if self.household_member.is_minor and self.guardian.lower() != 'yes':
            loss_reason.append('Minor without guardian available.')
        if loss_reason:
            if Loss.objects.filter(household_member=self.household_member):
                loss = Loss.objects.get(household_member=self.household_member)
                loss.report_datetime = datetime.today()
                loss.loss_reason = loss_reason
            else:
                Loss.objects.create(
                    household_member=self.household_member,
                    report_datetime=datetime.today(),
                    reason=';'.join(loss_reason))
        return loss_reason

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Enrolment Checklist"
