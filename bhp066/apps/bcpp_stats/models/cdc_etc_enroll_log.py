from django.db import models

from edc.core.crypto_fields.fields import EncryptedIdentityField

from .base_cdc import BaseCdc


class CdcEtcEnrollLog(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    enrolldt = models.DateField()
    partid = models.CharField(max_length=25, null=True)
    omang = EncryptedIdentityField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
