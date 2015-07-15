from django.db import models

from edc.constants import NOT_APPLICABLE
from edc.audit.audit_trail import AuditTrail

from .base_sexual_partner import BaseSexualPartner


class MonthsSecondPartner (BaseSexualPartner):
    """A model completed by the user on the participant's recent sexual behaviour."""

    second_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
                )
    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.second_partner_arm = self.is_ecc_or_cpc() if self.is_ecc_or_cpc() else NOT_APPLICABLE\
                                                            if self.sex_partner_community == NOT_APPLICABLE else\
                                                                    'OTHER' if self.sex_partner_community == 'OTHER' else ''
        super(MonthsSecondPartner, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Second Partner - 12 Months"
        verbose_name_plural = "Second Partner - 12 Months"
