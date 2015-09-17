from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import date_not_future
from edc.base.model.fields import OtherCharField

from bhp066.apps.bcpp.choices import DXTB_CHOICE

from .base_scheduled_visit_model import BaseScheduledVisitModel


class Tubercolosis (BaseScheduledVisitModel):

    """A model completed by the user to record any diagnosis of
    Tuberculosis in the past 12 months."""

    date_tb = models.DateField(
        verbose_name=_("Date of the diagnosis of tuberculosis:"),
        validators=[date_not_future],
        help_text="",
    )

    dx_tb = models.CharField(
        verbose_name=_("[Interviewer:]What is the tuberculosis diagnosis as recorded?"),
        max_length=50,
        choices=DXTB_CHOICE,
        help_text="",
    )
    dx_tb_other = OtherCharField(
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Tubercolosis"
        verbose_name_plural = "Tubercolosis"
