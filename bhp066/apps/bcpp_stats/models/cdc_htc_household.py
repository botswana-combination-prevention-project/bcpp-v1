from django.db import models

from .base_cdc import BaseCdc


class CdcHtcHousehold(BaseCdc):

    Community_Name = models.CharField(max_length=25, null=True)
    Enum_Status_Code = models.CharField(max_length=50, null=True)
    GPS_acc_meters = models.IntegerField(null=True)
    HH_Status_Code = models.CharField(max_length=50, null=True)
    NmbrStxr_OnMap_Ind = models.CharField(max_length=50, null=True)
    Visit_Date = models.DateField(null=True)
    hh_id = models.CharField(max_length=25, null=True)
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
