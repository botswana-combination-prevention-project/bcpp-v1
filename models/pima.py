from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bhp_common.choices import YES_NO
from base_scheduled_visit_model import BaseScheduledVisitModel


class Pima (BaseScheduledVisitModel):

    """CS002 - Used for PIMA cd4 count recording"""

    cd4_value = models.DecimalField(
        verbose_name=_("What is the CD4 count of the PIMA machine?"),
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        help_text="",
        )

    draw_time = models.TimeField(
        verbose_name=_("What is the time of the PIMA machine blood draw?"),
        )

    is_drawn = models.CharField(
        verbose_name=_("Was a finger prick done today?"),
        choices=YES_NO,
        max_length=3,
        help_text="",
        )
    is_drawn_other = OtherCharField(
        verbose_name=_("If no finger prick today, please explain why"),
        null=True,
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "PIMA CD4 count"
        verbose_name_plural = "PIMA CD4 count"
