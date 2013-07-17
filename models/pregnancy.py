from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import ANCREG_CHOICE
from base_pregnancy import BasePregnancy


class Pregnancy (BasePregnancy):

    """CS002 - Meant for women who are currently pregnant"""

    anc_reg = models.CharField(
        verbose_name="Have you registered for antenatal care?",
        max_length=55,
        null=True,
        blank=True,
        choices=ANCREG_CHOICE,
        help_text="",
        )

    lnmp = models.DateField(
        verbose_name="When was your last normal menstrual period?",
        help_text="",
        )

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_pregnancy_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Pregnancy"
        verbose_name_plural = "Pregnancy"
