from django.db import models

from .base_cdc import BaseCdc


class CdcReferralLog(BaseCdc):

    crf_name = models.CharField(max_length=50, null=True)
    event_crf_id = models.IntegerField()
    event_id = models.IntegerField(null=True)
    event_name = models.CharField(max_length=25, null=True)
    oc_study_id = models.CharField(max_length=25, null=True)
    ssid = models.CharField(max_length=25)
    study_indentifier = models.CharField(max_length=25, null=True)
    study_name = models.CharField(max_length=25, null=True)

    RefOutcome = models.IntegerField(null=True)
    RefSource = models.IntegerField(null=True)
    RefType = models.IntegerField(null=True)
    ScreenEnroll = models.IntegerField(null=True)
    VisitRsn = models.IntegerField(null=True)
    staff_id = models.IntegerField(null=True)
    studyid = models.CharField(max_length=25, null=True)
    visit_date = models.DateField(null=True)

    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
