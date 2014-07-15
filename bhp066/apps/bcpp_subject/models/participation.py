from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.core.crypto_fields.fields import EncryptedTextField
from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO
from edc.subject.appointment.models import BaseParticipationModel

from .base_scheduled_visit_model import BaseScheduledVisitModel


class Participation (BaseScheduledVisitModel, BaseParticipationModel):

    full = models.CharField(
        verbose_name=_('Has the participant agreed to fully participate in BHS'),
        max_length=15,
        choices=YES_NO,
        default='Yes',
        )

    description = EncryptedTextField(
        verbose_name="Describe *what the participant chose to participate in and *what they rejected.",
        max_length=250,
        blank=True,
        null=True,
        )

    history = AuditTrail()

    def allow_missing_forms(self):
        if self.full.lower() == 'no':
            return True
        return False

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Participation"
        verbose_name_plural = "Participation"
