from django.db import models

from edc_base.encrypted_fields import IdentityField
from .base_cdc import BaseCdc


class CdcEnrollLog(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    enrolldt = models.DateField(null=True)
    omang = IdentityField(null=True)
    partid = models.CharField(
        max_length=25,
        null=True,
        help_text='Participant Identifier, e.g. BHS subject_identifier, HTC, etc')

    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
