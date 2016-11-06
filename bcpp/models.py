from django.db import models

from edc_registration.model_mixins import RegisteredSubjectModelMixin
from edc_base.model.models import BaseUuidModel


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'bcpp'


class AvailablePlot(BaseUuidModel):

    """A model used to limit plots shown by the model manager.

    Formerly named 'NotebookPlotList'.
    """

    plot_identifier = models.CharField(
        verbose_name='Plot Identifier',
        max_length=25,
        unique=True)

    community = models.CharField(
        max_length=25)

    device_id = models.IntegerField()

    class Meta:
        app_label = 'bcpp'
