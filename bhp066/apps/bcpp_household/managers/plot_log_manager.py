from datetime import timedelta

from django.conf import settings
from django.db import models

from edc.map.classes import site_mappers

from ..classes import PlotIdentifier


class PlotLogManager(models.Manager):

    def get_by_natural_key(self, plot_identifier):
        Plot = models.get_model('bcpp_household', 'Plot')
        plot = Plot.objects.get_by_natural_key(plot_identifier)
        return self.get(plot=plot)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.current_mapper.map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(
                    PlotLogManager, self).get_queryset().filter(
                        plot__community=community, plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists())
            else:
                return super(PlotLogManager, self).get_queryset().filter(plot__community=community)
        return super(PlotLogManager, self).get_queryset()


class PlotLogEntryManager(models.Manager):

    def get_by_natural_key(self, report_datetime, plot_identifier):
        PlotLog = models.get_model('bcpp_household', 'PlotLog')
        plot_log = PlotLog.objects.get_by_natural_key(plot_identifier)
        margin = timedelta(microseconds=999)
        return self.get(report_datetime__range=(
            report_datetime - margin, report_datetime + margin),
            plot_log=plot_log)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.current_mapper.map_area
            if PlotIdentifier.get_notebook_plot_lists():
                return super(PlotLogEntryManager, self).get_queryset().filter(
                    plot_log__plot__community=community,
                    plot_log__plot__plot_identifier__in=PlotIdentifier.get_notebook_plot_lists(),
                )
            else:
                return super(PlotLogEntryManager, self).get_queryset().filter(plot_log__plot__community=community)
        return super(PlotLogEntryManager, self).get_queryset()
