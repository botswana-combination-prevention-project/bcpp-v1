from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import GENDER
from edc.choices.common import YES_NO, YES_NO_DWTA, YES_NO_NA
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from .household_member import HouseholdMember


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
        validators=[eligible_if_yes, ],
        help_text="Allow Omang, Passport number, driver's license number or Omang receipt number. If 'NO', STOP participant cannot be enrolled"
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
        help_text="If 'NO', STOP participant cannot be enrolled",
        )

    marriage_certificate = models.CharField(
        verbose_name=("[Interviewer] Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default='N/A',
        help_text="If 'NO', STOP participant cannot be enrolled",
        )

    marriage_certificate_no = models.CharField(
        verbose_name=("What is the marriage certificate number?"),
        max_length=9,
        null=True,
        blank=True,
        help_text="e.g. 000/YYYY",
        )

    part_time_resident = models.CharField(
        verbose_name=("In the past 12 months, have you typically spent 3 or"
                      " more nights per month in this community? "),
        max_length=10,
        choices=YES_NO_DWTA,
        validators=[eligible_if_yes, ],
        help_text=("If participant has moved into the "
                  "community in the past 12 months, then "
                  "since moving in has the participant typically "
                  "spent more than 3 nights per month in this community. "
                  "If 'NO (or don't want to answer)' STOP. Participant cannot be enrolled."),
        )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        """Does not save anything, note no call to super."""
        self.household_member.eligible_subject = True
        self.household_member.save()

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Enrolment Checklist"
