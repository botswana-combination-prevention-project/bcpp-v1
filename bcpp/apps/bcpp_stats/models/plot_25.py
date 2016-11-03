from django.db import models

from .base_cdc import BaseCdc


class Plot25(BaseCdc):

    plot_identifier = models.CharField(max_length=25, null=True)
    action = models.CharField(max_length=25, null=True)
    status = models.CharField(max_length=25, null=True)
    household_count = models.CharField(max_length=25, null=True)
    gps_target_lat = models.FloatField(null=True)
    gps_target_lon = models.FloatField(null=True)
    enrolled = models.CharField(max_length=25, null=True)
    comment = models.CharField(max_length=250, null=True)

    class Meta:
        app_label = 'bcpp_stats'
