from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..managers import ReplacementHistoryManager


class ReplacementHistory(BaseDispatchSyncUuidModel):
    """A model that records the history of plots and households that have
    been selected for replacement and replaced by a plot from the pool
    of available plots (5%)."""
    replacing_item = models.CharField(
        verbose_name='Plot identifier of the plot that replaced a household or plot',
        max_length=25,
        )

    replaced_item = models.CharField(
        verbose_name='Plot or household identifier replaced',
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
