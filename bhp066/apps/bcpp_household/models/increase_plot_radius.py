from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.device.dispatch.models import DispatchItemRegister

from .plot import Plot


class IncreasePlotRadius(BaseDispatchSyncUuidModel):
    """A model completed by the user to allow a plot\'s GPS target radius to be changed.

    An instance is auto created once the criteria is met. See method plot.increase_plot_radius."""
    plot = models.OneToOneField(Plot)

    radius = models.FloatField(
        default=25.0,
        help_text='meters')

    history = AuditTrail()

    def __unicode__(self):
        return self.plot.plot_identifier

    def natural_key(self):
        return (self.plot.plot_identifier, )

    def dispatch_container_lookup(self):
        dispatch_container = models.get_model('dispatch', 'DispatchContainerRegister')
        if dispatch_container.objects.filter(
                container_identifier=self.plot.plot_identifier, is_dispatched=True).exists():
            return dispatch_container.objects.get(
                container_identifier=self.plot.plot_identifier, is_dispatched=True)
        return None

    def include_for_dispatch(self):
        return True

    @property
    def producer(self):
        try:
            dispatch_item_register = DispatchItemRegister.objects.using('default').get(item_pk=self.plot.pk)
            return dispatch_item_register.producer
        except DispatchItemRegister.DoesNotExist:
            return None

    @property
    def action(self):
        return self.plot.action

    @property
    def bypass_radius(self):
        return self.radius

    @property
    def status(self):
        return self.plot.status

    class Meta:
        app_label = 'bcpp_household'
