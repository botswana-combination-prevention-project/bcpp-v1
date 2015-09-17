from django.db import models

from edc.constants import NOT_APPLICABLE
from edc_base.audit_trail import AuditTrail

from .base_sexual_partner import BaseSexualPartner


class MonthsThirdPartner (BaseSexualPartner):
    """A model completed by the user on the participant's recent sexual behaviour."""

    third_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
                )
    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.third_partner_arm = self.is_ecc_or_cpc() if self.is_ecc_or_cpc() else NOT_APPLICABLE\
                                                            if self.sex_partner_community == NOT_APPLICABLE else\
                                                                    'OTHER' if self.sex_partner_community == 'OTHER' else ''
        super(MonthsThirdPartner, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Third Partner - 12 Months"
        verbose_name_plural = "Third Partner - 12 Months"
