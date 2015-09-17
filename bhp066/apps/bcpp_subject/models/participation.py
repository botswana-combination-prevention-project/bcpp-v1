from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO

from bhp066.apps.bcpp.choices import PARTIAL_PARTICIPATION_TYPE

from .base_scheduled_visit_model import BaseScheduledVisitModel


class Participation (BaseScheduledVisitModel):

    full = models.CharField(
        verbose_name=_('Has the participant agreed to fully participate in BHS'),
        max_length=15,
        choices=YES_NO,
        default='Yes',
    )

    participation_type = models.CharField(
        verbose_name=_("What type of partial participation did the client choose?"),
        max_length=30,
        choices=PARTIAL_PARTICIPATION_TYPE,
    )

    history = AuditTrail()

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Participation"
        verbose_name_plural = "Participation"
