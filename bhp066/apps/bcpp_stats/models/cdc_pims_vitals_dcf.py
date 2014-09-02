from django.db import models

from .base_cdc import BaseCdc


class CdcPimsVitalsDcf(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    visit_date = models.DateField(null=True)
    ARTRX_Regimen = models.IntegerField(null=True)
    Med_ARV = models.IntegerField(null=True)
    Med_Regimen = models.IntegerField(null=True)
    SRH_PMTCT = models.IntegerField(null=True)
    artrx_regimenother = models.IntegerField(null=True)
    artrx_startdt = models.DateField(null=True)
    med_regimenother = models.CharField(max_length=25, null=True)
    srh_pmtctdt = models.DateField(null=True)

    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
