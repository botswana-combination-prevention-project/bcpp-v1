from django.apps import apps as django_apps
from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin
from datetime import timedelta


class PlotLogManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = ['plot']

    def get_by_natural_key(self, plot_identifier):
        Plot = django_apps.get_model('bcpp_household', 'Plot')
        plot = Plot.objects.get_by_natural_key(plot_identifier)
        return self.get(plot=plot)


class PlotLogEntryManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = ['plot_log', 'plot']

    def get_by_natural_key(self, report_datetime, plot_identifier):
        PlotLog = django_apps.get_model('bcpp_household', 'PlotLog')
        plot_log = PlotLog.objects.get_by_natural_key(plot_identifier)
        margin = timedelta(microseconds=999)
        return self.get(report_datetime__range=(
            report_datetime - margin, report_datetime + margin),
            plot_log=plot_log)
