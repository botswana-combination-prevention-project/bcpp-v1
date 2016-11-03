from django.db import models

from .base_cdc import BaseCdc


class CdcHtc(BaseCdc):

    Visit_Date = models.DateField(null=True)

    Community_Name = models.CharField(max_length=15, null=True)

    hh_id = models.CharField(max_length=15, null=True)

    HH_Status_Code = models.CharField(max_length=15, null=True)

    Enum_Status_Code = models.CharField(max_length=15, null=True)

    HHM_GENDER = models.CharField(max_length=15, null=True)

    HHM_NIGHTS_OUTSIDE = models.IntegerField(null=True)

    HHM_AGE = models.IntegerField(null=True)

    Visit_Status = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'bcpp_stats'
