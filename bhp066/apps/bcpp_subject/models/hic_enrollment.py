from django.db import models
from edc.audit.audit_trail import AuditTrail
from apps.bcpp.choices import YES_NO

from .base_scheduled_visit_model import BaseScheduledVisitModel


class HicEnrollment (BaseScheduledVisitModel):

    hic_permission = models.CharField(
        verbose_name="Is it okay for the project to visit you every year for the next three years for further questions and testing?",
        max_length=25,
        choices=YES_NO,
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Hic Enrollement"
        verbose_name_plural = "Hic Enrollement"
