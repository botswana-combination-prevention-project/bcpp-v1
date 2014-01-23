from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import eligible_if_yes, eligible_if_positive
from edc.choices.common import YES_NO_DWTA
from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge

from apps.bcpp.choices import VERBALHIVRESULT_CHOICE

from .base_clinic_registered_subject_model import BaseClinicRegisteredSubjectModel


class ClinicEligibility (BaseClinicRegisteredSubjectModel):

    dob = models.DateField(
        verbose_name=_("Date of birth"),
        validators=[
            dob_not_future,
            MinConsentAge,
            MaxConsentAge,
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

    history = AuditTrail()

    def get_registration_datetime(self):
        return self.registration_datetime

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Eligibility"
        verbose_name_plural = "Clinic Eligibility"
