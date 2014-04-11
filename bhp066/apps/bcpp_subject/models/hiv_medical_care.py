from django.db import models
from edc.base.model.validators import date_not_future
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail

from apps.bcpp.choices import LOWESTCD4_CHOICE

from .base_scheduled_visit_model import BaseScheduledVisitModel


class HivMedicalCare (BaseScheduledVisitModel):

    first_hiv_care_pos = models.DateField(
        verbose_name=_("When did you first receive HIV-related medical care "
                       "for such things as a CD4 count (masole), IDCC/ PMTCT "
                       "registration, additional clinic-based counseling?"),
        validators=[date_not_future],
        max_length=25,
        null=True,
        blank=True,
        help_text=_("Note: If participant does not want to answer, leave blank.  "
                   "If participant is unable to estimate date, leave blank."),
        )

    last_hiv_care_pos = models.DateField(
        verbose_name=_("When did you last (most recently) receive HIV-related "
                      "medical care for such things as a CD4 count (masole), "
                      "IDCC/ PMTCT registration, additional clinic-based counseling?"),
        validators=[date_not_future],
        max_length=25,
        null=True,
        blank=True,
        help_text=_("Note: If participant does not want to answer,leave blank. "
                   "If participant is unable to estimate date, leave blank."),
        )

    lowest_cd4 = models.CharField(
        verbose_name=_("What was your lowest CD4 (masole) count that was ever measured?"),
        max_length=25,
        choices=LOWESTCD4_CHOICE,
        help_text=_("Assist the participant by helping review their outpatient cards if "
                   "they are available."),
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Medical care"
        verbose_name_plural = "HIV Medical care"
