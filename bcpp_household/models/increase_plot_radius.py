from django.db import models

from simple_history.models import HistoricalRecords as AuditTrail
from edc_sync.model_mixins import SyncModelMixin
from edc_base.model.models import BaseUuidModel

from .plot import Plot


class IncreasePlotRadius(SyncModelMixin, BaseUuidModel):
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
