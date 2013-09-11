import socket
from django.db import models
from django.db.models import Max
from bhp_variables.models import StudySpecific
from bhp_netbook.models import Netbook


class PlotManager(models.Manager):

    def get_by_natural_key(self, plot_identifier):
        return self.get(plot_identifier=plot_identifier)
