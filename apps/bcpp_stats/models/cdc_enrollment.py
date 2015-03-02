from django.db import models

from .base_cdc import BaseCdc


class CdcEnrollment(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    form_date = models.DateField(null=True)
    ARTHx_ARVEver = models.IntegerField(null=True)
    ARTHx_ARVPresent = models.IntegerField(null=True)
    ART_BF_Continue = models.IntegerField(null=True)
    ART_BF_Initiate = models.IntegerField(null=True)
    ART_Consent_OutBW = models.IntegerField(null=True)
    ART_Elig_OutBW = models.IntegerField(null=True)
    ART_Regimen = models.CharField(max_length=25, null=True)
    ART_VL_Initiate = models.IntegerField(null=True)
    BHSverf_CD4 = models.IntegerField(null=True)
    BHSverf_postatus = models.IntegerField(null=True)
    HDMH_Preg = models.IntegerField(null=True)
    VL_Result = models.IntegerField(null=True)
    VL_ResultNum = models.IntegerField(null=True)
    appt_date = models.DateField(null=True)
    art_regimenother = models.CharField(max_length=25, null=True)
    art_startdate = models.DateField(null=True)
    bhsverf_cd4dt = models.DateField(null=True)
    bhsverf_refdt = models.DateField(null=True)
    comp_date = models.DateField(null=True)
    sd_gender = models.IntegerField(null=True)
    vl_testdate = models.DateField(null=True)

    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
