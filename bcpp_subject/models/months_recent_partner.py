from edc_base.audit_trail import AuditTrail

from django.db import models

from .base_sexual_partner import BaseSexualPartner
from .subject_consent import SubjectConsent


class MonthsRecentPartner (BaseSexualPartner):
    """A model completed by the user on the participant's recent sexual behaviour."""

    CONSENT_MODEL = SubjectConsent

    first_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.first_partner_arm = self.get_partner_arm()
        super(MonthsRecentPartner, self).save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Recent Partner - 12 Months"
        verbose_name_plural = "Recent Partner - 12 Months"
