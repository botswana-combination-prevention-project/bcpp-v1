from django.db import models

from .base_cdc import BaseCdc


class CdcFollowup(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    form_date = models.DateField(null=True)

    ARTALL_Elig = models.IntegerField(null=True)
    ARTCPC_ContPregBF = models.IntegerField(null=True)
    ARTCPC_InitPregBF = models.IntegerField(null=True)
    CAE_BWGuide = models.IntegerField(null=True)
    CAE_BWGuideType = models.IntegerField(null=True)
    CAE_BWOutConsent = models.IntegerField(null=True)
    CAE_Regimen = models.IntegerField(null=True)
    CAE_VL_PrgBF = models.IntegerField(null=True)
    LAB_CD4 = models.IntegerField(null=True)
    STT_tx = models.IntegerField(null=True)
    VT_AE = models.IntegerField(null=True)
    VT_Unschvisit = models.IntegerField(null=True)
    VT_Visittype = models.IntegerField(null=True)
    VT_visitmonth = models.IntegerField(null=True)
    cae_artdate = models.DateField(null=True)
    comp_date = models.DateField(null=True)
    lab_cd4_date = models.DateField(null=True)

    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
