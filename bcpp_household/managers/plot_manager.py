from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class PlotManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = []

    def get_by_natural_key(self, plot_identifier):
        return self.get(plot_identifier=plot_identifier)
