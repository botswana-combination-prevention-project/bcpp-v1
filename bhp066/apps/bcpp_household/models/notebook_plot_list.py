from django.db import models
from django.utils.translation import ugettext as _

from edc.base.model.models import BaseUuidModel


class NotebookPlotList(BaseUuidModel):

    plot_identifier = models.CharField(
        verbose_name='Plot Identifier',
        max_length=25,
        unique=True,
        help_text=_("Plot identifier"),
        editable=True,)

    class Meta:
        app_label = 'bcpp_household'
