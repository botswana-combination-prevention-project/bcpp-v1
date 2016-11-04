from django.db import models

from edc_sync.model_mixins import SyncModelMixin
from edc_base.model.models import BaseUuidModel


class NotebookPlotList(SyncModelMixin, BaseUuidModel):
    # TODO: Dispatch

    plot_identifier = models.CharField(
        verbose_name='Plot Identifier',
        max_length=25,
        unique=True,
        help_text="Plot identifier",
        editable=True,)

    def natural_key(self):
        return (self.plot_identifier, )

    def is_serialized(self):
        return False

    def dispatch_container_lookup(self, using=None):
        return (self.__class__, 'plot_identifier')

    def is_dispatch_container_model(self):
        return False

    def dispatched_as_container_identifier_attr(self):
        return 'plot_identifier'

    class Meta:
        app_label = 'bcpp_household'
