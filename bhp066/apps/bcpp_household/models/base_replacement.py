from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from .plot import Plot


class BaseReplacement(BaseDispatchSyncUuidModel):

    history = AuditTrail()

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-household_identifier', ]
