from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future

from bhp066.apps.bcpp_list.models import HeartDisease

from .base_scheduled_visit_model import BaseScheduledVisitModel


class HeartAttack (BaseScheduledVisitModel):

    """A model completed by the user to record any heart conditions in the past 12 months."""

    date_heart_attack = models.DateField(
        verbose_name=_("Date of the heart disease or stroke diagnosis:"),
        validators=[date_not_future],
        help_text="",
    )

    dx_heart_attack = models.ManyToManyField(HeartDisease,
        verbose_name=_("[Interviewer:] What is the heart disease or stroke diagnosis as recorded?"),
        help_text=("(tick all that apply)"),
    )

    dx_heart_attack_other = OtherCharField()

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Heart Attack or Stroke"
        verbose_name_plural = "Heart Attack or Stroke"
