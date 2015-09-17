from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..managers import ReplacementHistoryManager


class ReplacementHistory(BaseDispatchSyncUuidModel):
    """A system model that tracks replaced, and replaced by, plots and households."""
    replacing_item = models.CharField(
        verbose_name='Replaced by',
        max_length=25,
    )

    replaced_item = models.CharField(
        verbose_name='Replaced item',
        max_length=25,
    )

    replacement_datetime = models.DateTimeField()

    replacement_reason = models.CharField(
        verbose_name='Reason for replacement',
        max_length=100,
        help_text=_("Reasons could be absentees, refusals, e.t.c"),
    )

    history = AuditTrail()

    objects = ReplacementHistoryManager()

    def natural_key(self):
        return (self.replacing_item, self.replaced_item)

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-replacing_item', ]
        unique_together = ('replacing_item', 'replaced_item')
