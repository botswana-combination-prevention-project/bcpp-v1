from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO
from base_scheduled_htc_visit import BaseScheduledHtcVisit


class HtcCircumcision (BaseScheduledHtcVisit):

    """For males only"""

    is_circumcised = models.CharField(
        verbose_name=_("Male circumcision is the removal of the foreskin of "
                       "the penis.  Here is a diagram to clarify what a "
                       "circumcised and uncircumcised man looks like. "
                       "Are you circumcised? "),
        max_length=3,
        choices=YES_NO,
        help_text="",
        )

    circumcision_year = models.DateField(
        verbose_name=_("What year were you circumcised? "),
        null=True,
        blank=True,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc'
        verbose_name = "HTC Circumcision"
        verbose_name_plural = "HTC Circumcision"
