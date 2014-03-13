from datetime import timedelta
from django.db import models


class PlotLogManager(models.Manager):

    def get_by_natural_key(self, plot_identifier):
        Plot = models.get_model('bcpp_household', 'Plot')
        plot = Plot.objects.get_by_natural_key(plot_identifier)
        return self.get(plot=plot)


class PlotLogEntryManager(models.Manager):

    def get_by_natural_key(self, report_datetime, plot_identifier):
        PlotLog = models.get_model('bcpp_household', 'PlotLog')
        plot_log = PlotLog.objects.get_by_natural_key(plot_identifier)
        margin = timedelta(microseconds=999)
        return self.get(report_datetime__range=(report_datetime - margin, report_datetime + margin), plot_log = plot_log)
