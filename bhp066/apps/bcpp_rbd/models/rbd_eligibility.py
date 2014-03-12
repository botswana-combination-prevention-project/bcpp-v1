from django.db import models
from django.utils.translation import ugettext as _

from edc.base.model.validators import dob_not_future, MinConsentAge
from edc.base.model.validators import eligible_if_yes, eligible_if_positive
from edc.choices.common import YES_NO_DWTA
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

    objects = models.Manager()

    def save(self, *args, **kwargs):
        """Does not save anything, note no call to super."""
        self.household_member.eligible_rbd_subject = True
        self.household_member.save()

    class Meta:
        app_label = "bcpp_rbd"
        verbose_name = "Research Blood Draw Eligibility"
