from django.db import models

from .plot import Plot

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel


class IncreasePlotRadius(BaseDispatchSyncUuidModel):

    plot = models.ForeignKey(Plot)

    radius = models.FloatField(default=25.0, help_text='meters')

    history = AuditTrail()

    def __unicode__(self):
        return self.plot.plot_identifier

    def natural_key(self):
        return (self.plot.plot_identifier,)

    def save(self, *args, **kwargs):
        self.plot.target_radius = (self.radius / 1000)
        self.plot.save()
        super(IncreasePlotRadius, self).save(*args, **kwargs)

    def dispatch_container_lookup(self):
        dispatch_container = models.get_model('dispatch', 'DispatchContainerRegister')
        if dispatch_container.objects.filter(container_identifier=self.plot.plot_identifier, is_dispatched=True).exists():
            return dispatch_container.objects.get(container_identifier=self.plot.plot_identifier, is_dispatched=True)
        return None

    def include_for_dispatch(self):
        return True

    class Meta:
        app_label = 'bcpp_household'
