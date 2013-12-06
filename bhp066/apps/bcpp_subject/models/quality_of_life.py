from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail

from ..choices import MOBILITY, SELF_CARE, ACTIVITIES, PAIN, ANXIETY

from .base_scheduled_visit_model import BaseScheduledVisitModel


class QualityOfLife (BaseScheduledVisitModel):

    """CE001"""

    mobility = models.CharField(
        verbose_name=_("Mobility"),
        max_length=45,
        choices=MOBILITY,
        help_text="",
        )
    self_care = models.CharField(
        verbose_name=_("Self-Care"),
        max_length=65,
        choices=SELF_CARE,
        help_text="",
        )
    activities = models.CharField(
        verbose_name=_("Usual Activities (e.g. work, study, housework, family or leisure activities)"),
        max_length=50,
        choices=ACTIVITIES,
        help_text="",
        )
    pain = models.CharField(
        verbose_name=_("Pain / Discomfort "),
        max_length=35,
        choices=PAIN,
        help_text="",
        )
    anxiety = models.CharField(
        verbose_name=_("Anxiety / Depression "),
        max_length=40,
        choices=ANXIETY,
        help_text="",
        )
    health_today = models.IntegerField(
        verbose_name=_("We would like to know how good or bad your health is TODAY. "
                      "This scale is numbered from 0 to 100. 100 means the 'best' health"
                      " you can imagine. 0 means the 'worst' health you can imagine. "
                      "Indicate on the scale how your health is TODAY.  "),
        max_length=3,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text=("Note:Interviewer, please record corresponding number in the boxes."
                   " If participant does not want to answer, leave blank"),
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Quality of Life"
        verbose_name_plural = "Quality of Life"
