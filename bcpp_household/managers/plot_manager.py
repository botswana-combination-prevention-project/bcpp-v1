from django.conf import settings
from django.db import models

from edc_map.site_mappers import site_mappers

from ..plot_identifier import PlotIdentifier


class PlotManager(models.Manager):

    def get_by_natural_key(self, plot_identifier):
        return self.get(plot_identifier=plot_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(PlotManager, self).get_queryset().filter(
                    community=community, plot_identifier__in=PlotIdentifier.get_notebook_plot_lists())
            else:
                return super(PlotManager, self).get_queryset().filter(community=community)
        return super(PlotManager, self).get_queryset()
