from django.db import models

from .base_cdc import BaseCdc


class CdcPimsLabDcf(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    visit_date = models.DateField(null=True)
    CD4VL_CD4Rslt = models.IntegerField(null=True)
    CD4VL_CD4Source = models.IntegerField(null=True)
    CD4VL_NewCD4 = models.IntegerField(null=True)
    CD4VL_NewVL = models.IntegerField(null=True)
    CD4VL_VLRsltCpies = models.IntegerField(null=True)
    CD4VL_VLRslt_v1 = models.IntegerField(null=True)
    CD4VL_VLRslt_v2 = models.IntegerField(null=True)
    cd4vl_cd4dt = models.DateField(null=True)
    cd4vl_cd4rsltdt = models.DateField(null=True)
    cd4vl_vldt = models.DateField(null=True)
    cd4vl_vlrsltdt = models.DateField(null=True)

    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
