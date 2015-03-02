from django.db import models

from .base_cdc import BaseCdc


class CdcEtcEnroll(BaseCdc):

    event_crf_id = models.IntegerField()
    ssid = models.CharField(max_length=25)
    oc_study_id = models.CharField(max_length=25, null=True)
    crf_name = models.CharField(max_length=50, null=True)
    art_regimen = models.IntegerField(null=True)
    art_regimenother = models.CharField(max_length=25, null=True)
    art_startdate = models.DateField(null=True)
    arthx_arvever = models.IntegerField(null=True)
    arthx_arvpresent = models.CharField(max_length=25, null=True)
    cdemo_age = models.IntegerField(null=True)
    cdemo_dob = models.DateField(null=True)
    comp_date = models.DateField(null=True)
    form_date = models.DateField(null=True)
    outbw_gender = models.IntegerField(null=True)
    outbw_preg = models.IntegerField(null=True)
    outbw_pregbf = models.IntegerField(null=True)
    outbw_pregbfcontinue = models.IntegerField(null=True)
    outbw_pregbfinitiate = models.IntegerField(null=True)
    outbw_testdate = models.DateField(null=True)
    outbw_vl = models.IntegerField(null=True)
    outbw_vlinitiate = models.IntegerField(null=True)
    ref_cd4dt = models.DateField(null=True)
    ref_date = models.DateField(null=True)
    ref_from = models.IntegerField(null=True)
    ref_postatus = models.IntegerField(null=True)
    res_future = models.IntegerField(null=True)
    res_past = models.IntegerField(null=True)
    sdemo_gender = models.CharField(max_length=25, null=True)
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)
    Ref_CD4 = models.IntegerField(null=True)
    OutBW_VLResults = models.IntegerField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
