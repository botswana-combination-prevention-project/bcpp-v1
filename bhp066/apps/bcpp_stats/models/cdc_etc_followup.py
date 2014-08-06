from django.db import models

from .base_cdc import BaseCdc


class CdcEtcFollowup(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    comp_date = models.DateField()
    form_date = models.DateField()
    lab_cd4 = models.IntegerField(null=True)
    lab_cd4_date = models.DateField(null=True)
    stt_appt = models.IntegerField(null=True)
    vt_ae = models.IntegerField(null=True)
    vt_unschvisit = models.IntegerField(null=True)
    vt_visittype = models.IntegerField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
