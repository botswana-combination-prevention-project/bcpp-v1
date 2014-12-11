from django.conf import settings
from django.db import models

from edc.map.classes import site_mappers


class PlotManager(models.Manager):

    def get_by_natural_key(self, plot_identifier):
        return self.get(plot_identifier=plot_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.current_mapper.map_area
            return super(PlotManager, self).get_queryset().filter(community=community)
        return super(PlotManager, self).get_queryset()
