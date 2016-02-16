from django.conf import settings
from django.db import models

from edc.map.classes import site_mappers

from ..classes import PlotIdentifier


class ReplaceableManager(models.Manager):

    def get_by_natural_key(self, item_identifier):
        return self.get(item_identifier=item_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(ReplaceableManager, self).get_queryset().filter(
                    community=community, plot_identifier__in=PlotIdentifier.get_notebook_plot_lists())
            else:
                return super(ReplaceableManager, self).get_queryset().filter(community=community)
        return super(ReplaceableManager, self).get_queryset()
