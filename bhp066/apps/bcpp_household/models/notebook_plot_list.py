from django.db import models

from edc.device.sync.models import BaseSyncUuidModel
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from bhp066.apps.bcpp_survey.models.survey import Survey


class NotebookPlotList(BaseDispatchSyncUuidModel, BaseSyncUuidModel):

    plot_identifier = models.CharField(
        verbose_name='Plot Identifier',
        max_length=25,
        unique=True,
        help_text="Plot identifier",
        editable=True,)

    community = models.CharField(
        max_length=25,
        editable=False)

    survey = models.ForeignKey(Survey,)

    notebook = models.CharField(
        max_length=25,
        help_text="Hostname of the researcher's machine.",)

    status = models.CharField(
        verbose_name='Plot allocation status',
        max_length=35,
        default='not_allocated')

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
        unique_together = ('plot_identifier', 'community', 'survey', 'notebook')
