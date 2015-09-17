from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import date_not_future

from bhp066.apps.bcpp.choices import ANCREG_CHOICE

from .base_pregnancy import BasePregnancy


class Pregnancy (BasePregnancy):

    """A model completed by the user for pregnant participants."""

    anc_reg = models.CharField(
        verbose_name=_("Have you registered for antenatal care?"),
        max_length=55,
        null=True,
        blank=True,
        choices=ANCREG_CHOICE,
        help_text="",
    )

    lnmp = models.DateField(
        verbose_name=_("When was the first day of your last normal menstrual period?"),
        validators=[date_not_future],
        help_text="",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Pregnancy"
        verbose_name_plural = "Pregnancy"
