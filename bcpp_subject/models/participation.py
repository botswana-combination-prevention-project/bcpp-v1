from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_constants.choices import YES_NO

from bhp066.apps.bcpp.choices import PARTIAL_PARTICIPATION_TYPE

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class Participation (BaseScheduledVisitModel):

    CONSENT_MODEL = SubjectConsent

    full = models.CharField(
        verbose_name='Has the participant agreed to fully participate in BHS',
        max_length=15,
        choices=YES_NO,
        default='Yes',
    )

    participation_type = models.CharField(
        verbose_name="What type of partial participation did the client choose?",
        max_length=30,
        choices=PARTIAL_PARTICIPATION_TYPE,
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "Participation"
        verbose_name_plural = "Participation"
