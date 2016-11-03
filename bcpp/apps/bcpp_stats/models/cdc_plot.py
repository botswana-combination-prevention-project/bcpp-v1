from django.db import models

from .base_cdc import BaseCdc


class CdcPlot(BaseCdc):

    token = models.IntegerField(null=True)
    id = models.IntegerField(primary_key=True)
    startdate = models.DateField(null=True)
    startlanguage = models.CharField(max_length=25, null=True)
    submitdate = models.DateField(null=True)
    datestamp = models.DateField(null=True)
    lastpage = models.IntegerField(null=True)
    s596925x2x2 = models.DateField(null=True)
    s596925x2x3 = models.IntegerField(null=True)
    s596925x2x4 = models.IntegerField(null=True)
    s596925x2x5 = models.CharField(max_length=25, null=True)
    s596925x2x6 = models.IntegerField(null=True)
    s596925x4x27 = models.IntegerField(null=True)
    s596925x4x28 = models.DateField(null=True)
    s596925x4x39 = models.IntegerField(null=True)
    s596925x4x40 = models.DateField(null=True)
    s596925x5x29 = models.FloatField(null=True)
    s596925x5x30sq1_sq001 = models.CharField(max_length=25, null=True)
    s596925x5x30sq1_sq002 = models.IntegerField(null=True)
    s596925x5x30sq2_sq001 = models.CharField(max_length=25, null=True)
    s596925x5x30sq2_sq002 = models.IntegerField(null=True)
    s596925x5x30sq3_sq001 = models.CharField(max_length=25, null=True)
    s596925x5x30sq3_sq002 = models.IntegerField(null=True)
    s596925x5x30sq4_sq001 = models.CharField(max_length=25, null=True)
    s596925x5x30sq4_sq002 = models.IntegerField(null=True)
    s596925x5x30sq5_sq001 = models.CharField(max_length=25, null=True)
    s596925x5x30sq5_sq002 = models.IntegerField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
