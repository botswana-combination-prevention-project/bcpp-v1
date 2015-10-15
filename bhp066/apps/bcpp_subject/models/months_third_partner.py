from django.db import models

from edc_base.audit_trail import AuditTrail

from .base_sexual_partner import BaseSexualPartner
from .subject_consent import SubjectConsent


class MonthsThirdPartner (BaseSexualPartner):
    """A model completed by the user on the participant's recent sexual behaviour."""

    CONSENT_MODEL = SubjectConsent

    third_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.third_partner_arm = self.get_partner_arm()
        super(MonthsThirdPartner, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Third Partner - 12 Months"
        verbose_name_plural = "Third Partner - 12 Months"
