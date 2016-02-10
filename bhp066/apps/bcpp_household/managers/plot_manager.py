from django.conf import settings
from django.db import models

from edc.map.classes import site_mappers
from bhp066.apps.bcpp.app_configuration.classes import bcpp_app_configuration as app_config

from ..classes import PlotIdentifier


class PlotManager(models.Manager):

    def get_by_natural_key(self, plot_identifier):
        return self.get(plot_identifier=plot_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_current_mapper().map_area
            if device.is_notebook:
                return super(PlotManager, self).get_queryset().filter(
                    community=community, plot_identifier__in=app_config.notebook_plot_list)
            else:
                return super(PlotManager, self).get6789_queryset().filter(community=community)
        return super(PlotManager, self).get_queryset()
