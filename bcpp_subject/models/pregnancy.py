from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp.choices import ANCREG_CHOICE
from base_pregnancy import BasePregnancy


class Pregnancy (BasePregnancy):

    """CS002 - Meant for women who are currently pregnant"""

    anc_reg = models.CharField(
        verbose_name=_("Have you registered for antenatal care?"),
        max_length=55,
        null=True,
        blank=True,
        choices=ANCREG_CHOICE,
        help_text="",
        )

    lnmp = models.DateField(
        verbose_name=_("When was your last normal menstrual period?"),
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Pregnancy"
        verbose_name_plural = "Pregnancy"
