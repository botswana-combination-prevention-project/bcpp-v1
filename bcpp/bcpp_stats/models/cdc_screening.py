from django.db import models

from .base_cdc import BaseCdc


class CdcScreening(BaseCdc):

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
    ART_AnyRsn_ARV = models.IntegerField(null=True)
    BHSHTC_CD4 = models.IntegerField(null=True)
    Clin_CD4 = models.IntegerField(null=True)
    Res_Citizen = models.IntegerField(null=True)
    Res_Next12 = models.IntegerField(null=True)
    Res_PMTCTPPEP_ARV = models.IntegerField(null=True)
    Res_Past12 = models.IntegerField(null=True)
    bhshtc_cd4_dt = models.DateField(null=True)
    bhshtc_date = models.DateField(null=True)
    clin_cd4_dt = models.DateField(null=True)
    demo_dob = models.DateField(null=True)

    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
