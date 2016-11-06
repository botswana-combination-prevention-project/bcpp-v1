from simple_history.models import HistoricalRecords

from django.db import models

from .base_sexual_partner import BaseSexualPartner


class MonthsRecentPartner (BaseSexualPartner):
    """A model completed by the user on the participant's recent sexual behaviour."""

    first_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.first_partner_arm = self.get_partner_arm()
        super(MonthsRecentPartner, self).save(*args, **kwargs)

    class Meta(BaseSexualPartner.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Recent Partner - 12 Months"
        verbose_name_plural = "Recent Partner - 12 Months"
