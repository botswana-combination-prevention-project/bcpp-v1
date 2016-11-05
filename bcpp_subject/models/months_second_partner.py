from django.db import models

from edc_base.audit_trail import AuditTrail

from .base_sexual_partner import BaseSexualPartner
from .subject_consent import SubjectConsent


class MonthsSecondPartner (BaseSexualPartner):
    """A model completed by the user on the participant's recent sexual behaviour."""

    CONSENT_MODEL = SubjectConsent

    second_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.second_partner_arm = self.get_partner_arm()
        super(MonthsSecondPartner, self).save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Second Partner - 12 Months"
        verbose_name_plural = "Second Partner - 12 Months"
