from django.db import models
from django.utils.translation import ugettext as _

from edc.base.model.validators import dob_not_future, MinConsentAge
from edc.base.model.validators import eligible_if_yes, eligible_if_positive
from edc.choices.common import GENDER
from edc.choices.common import YES_NO, YES_NO_DWTA, YES_NO_NA
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp.choices import VERBALHIVRESULT_CHOICE
from apps.bcpp_household_member.models import HouseholdMember


class RBDEligibility (BaseDispatchSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember)

    dob = models.DateField(
        verbose_name=_("Date of birth"),
        validators=[
            dob_not_future,
            MinConsentAge,
            ],
        null=True,
        blank=False,
        help_text="Format is YYYY-MM-DD",
        )

    part_time_resident = models.CharField(
        verbose_name=_("In the past 12 months, have you typically spent 3 or"
                      " more nights per month in this community? "),
        max_length=25,
        choices=YES_NO_DWTA,
        validators=[eligible_if_yes, ],
        help_text=("If participant has moved into the "
                  "community in the past 12 months, then "
                  "since moving in has the participant typically "
                  "spent more than 3 nights per month in this community. "
                  "If 'NO (or don't want to answer)' STOP. Participant cannot be enrolled."),
        )

    hiv_status = models.CharField(
        verbose_name=_("Please tell me your current HIV status?"),
        max_length=30,
        null=True,
        blank=True,
        validators=[eligible_if_positive, ],
        choices=VERBALHIVRESULT_CHOICE,
        help_text="(verbal response)",
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
        help_text=("If participant has moved into the "
                  "community in the past 12 months, then "
                  "since moving in has the participant typically "
                  "spent more than 3 nights per month in this community. "
                  "If 'NO (or don't want to answer)'. Participant will not be enrolled."),
        )

    literacy = models.CharField(
        verbose_name=("Is the participant LITERATE?, or if ILLITRATE, is there a"
                      "  LITERATE witness available "),
        max_length=10,
        choices=YES_NO,
        help_text=("If participate is illitrate, confirm there is a literate"
                   "witness available otherwise participant will not be enrolled."),
        )

    mentally_incapacitated = models.CharField(
        verbose_name=("[Interviewer] In your opinion, Is the participant mentally incapacitated?"),
        max_length=10,
        choices=YES_NO,
        help_text=("If Yes, participant will not be enrolled"),
        )

    involuntary_incarceration = models.CharField(
        verbose_name=("[Interviewer] Is this participant involuntarily incarcerated?"),
        max_length=10,
        choices=YES_NO,
        help_text=("If Yes, participant will not be enrolled"),
        )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        """Does not save anything, note no call to super."""
        if self.has_identity.lower() == 'no':
            self.household_member.eligible_rbd_subject = False
            self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        elif self.part_time_resident.lower() != 'yes':
            self.household_member.eligible_rbd_subject = False
            self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        elif self.hiv_status.lower() != 'pos':
            self.household_member.eligible_rbd_subject = False
            self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        elif self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'no':
            self.household_member.eligible_rbd_subject = False
            self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        elif self.citizen.lower() == 'no' and self.legal_marriage.lower() == 'yes' and self.marriage_certificate.lower() == 'no':
            self.household_member.eligible_rbd_subject = False
            self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        elif self.literacy.lower() == 'no':
            self.household_member.eligible_rbd_subject = False
            self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        elif self.mentally_incapacitated.lower() == 'yes':
            self.household_member.eligible_rbd_subject = False
            self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        elif self.involuntary_incarceration.lower() == 'yes':
            self.household_member.eligible_rbd_subject = False
            self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        elif self.household_member.is_minor():
            if self.guardian != 'Yes':
                self.household_member.eligible_rbd_subject = False
                self.household_member.member_status_partial = 'NOT_ELIGIBLE'
        else:
            self.household_member.eligible_rbd_subject = True
        self.household_member.save()

    class Meta:
        app_label = "bcpp_rbd"
        verbose_name = "RBD Eligibility"
