from django.db import models
from django.utils.translation import ugettext as _
from edc_lib.audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class Circumcision (BaseScheduledVisitModel):

    """CS002"""

    circumcised = models.CharField(
        verbose_name=_("Are you circumcised?"),
        max_length=15,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Circumcision"
        verbose_name_plural = "Circumcision"
