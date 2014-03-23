from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO

from .base_scheduled_visit_model import BaseScheduledVisitModel


class Participation (BaseScheduledVisitModel):

    full = models.CharField(
        verbose_name=_('Has the participant agree to fully participate in BHS'),
        max_length=15,
        choices=YES_NO,
        default='Yes',
        )

    history = AuditTrail()

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Participation"
        verbose_name_plural = "Participation"
