from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..exceptions import AlreadyReplaced
from .household import Household
from .plot import Plot


class BaseReplacement(BaseDispatchSyncUuidModel):

    history = AuditTrail()

    def replaced(self, using=None):
        if isinstance(Household, self.instance) or isinstance(Plot, self.instance):
            if self.instance.replacement:
                return True
        elif self.replacement_container(self, using=None).replacement:
            return True
        return False

    def replacement_container(self, using=None):
        return False

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        if self.id:
            if self.replacement_container(using):
                raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
            if self.replaced(using):
                raise AlreadyReplaced('Model {0}-{1} is replaced.'.format(self._meta.object_name, self.pk))
        super(BaseReplacement, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-household_identifier', ]
