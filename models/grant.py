from django.db import models
from django.utils.translation import ugettext as _
from bhp_base_model.fields import OtherCharField
from audit_trail.audit import AuditTrail
from labour_market_wages import LabourMarketWages
from bcpp_subject.choices import GRANT_TYPE
from base_scheduled_inline_model import BaseScheduledInlineModel
from bcpp_subject.managers import GrantManager


class Grant(BaseScheduledInlineModel):
    """Inline for labour_market_wages."""
    labour_market_wages = models.ForeignKey(LabourMarketWages)

    grant_number = models.IntegerField(
        verbose_name=_("How many of each type of grant do you receive?"),
        max_length=2,
        )
    grant_type = models.CharField(
        verbose_name=_("Grant name"),
        choices=GRANT_TYPE,
        max_length=34,
        )
    other_grant = OtherCharField()

    history = AuditTrail()

    objects = GrantManager()

    def inline_parent(self):
        return self.labour_market_wages

    def natural_key(self):
        return (self.report_datetime, ) + self.labour_market_wages.natural_key()
    natural_key.dependencies = ['bcpp_subject.labourmarketwages', ]

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Grant"
        verbose_name_plural = "Grants"
