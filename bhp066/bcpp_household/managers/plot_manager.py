from django.db import models


class PlotManager(models.Manager):

    def get_by_natural_key(self, plot_identifier):
        return self.get(plot_identifier=plot_identifier)
