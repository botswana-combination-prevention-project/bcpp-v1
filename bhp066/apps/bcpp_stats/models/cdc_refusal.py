from django.db import models

from .base_cdc import BaseCdc


class CdcRefusal(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    form_date = models.DateField(null=True)
    comp_date = models.DateField(null=True)
    Group = models.IntegerField(null=True)
    Info_ReasNoStART = models.IntegerField(null=True)
    Info_Reason = models.IntegerField(null=True)
    Info_ReasonNoART = models.IntegerField(null=True)
    info_reasnostartothr = models.IntegerField(null=True)
    info_reasonnoartothr = models.IntegerField(null=True)
    info_reasonother = models.IntegerField(null=True)

    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
