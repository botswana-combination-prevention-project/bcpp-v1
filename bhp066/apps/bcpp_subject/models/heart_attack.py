from django.db import models
from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import date_not_future

from apps.bcpp_list.models import HeartDisease

from .base_scheduled_visit_model import BaseScheduledVisitModel


class HeartAttack (BaseScheduledVisitModel):

    """CS002 - Medical Diagonoses - Sub"""

    date_heart_attack = models.DateField(
        verbose_name="Date of the heart disease or stroke diagnosis:",
        validators=[date_not_future],
        help_text=("Note: Record date of first day of hospital admission or date the diagnosis "
                   "was documented in the OPD record."),
        )

    dx_heart_attack = models.ManyToManyField(HeartDisease,
        verbose_name="[Interviewer:] What is the heart disease or stroke diagnosis as recorded?",
        help_text=("Note: If record of diagnosis is not available, record the participant's "
                   "best knowledge. (tick all that apply)"),
        )
    dx_heart_attack_other = OtherCharField()

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Heart Attack"
        verbose_name_plural = "Heart Attack"
