from django.db import models
from bhp_base_model.fields import OtherCharField
from audit_trail.audit import AuditTrail
from labour_market_wages import LabourMarketWages
from bcpp_subject.choices import GRANT_TYPE
from base_scheduled_inline_model import BaseScheduledInlineModel


class Grant(BaseScheduledInlineModel):
    """Inline for labour_market_wages."""
    labour_market_wages = models.ForeignKey(LabourMarketWages)

    grant_number = models.IntegerField(
        verbose_name="How many of each type of grant do you receive?",
        max_length=2,
        )
    grant_type = models.CharField(
        verbose_name="Grant name",
        choices=GRANT_TYPE,
        max_length=34,
        )
    other_grant = OtherCharField()

    history = AuditTrail()

    def inline_parent(self):
        return self.labour_market_wages

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Grant"
        verbose_name_plural = "Grants"
