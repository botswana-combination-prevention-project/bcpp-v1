from django.db import models

from edc_base.encrypted_fields import IdentityField

from .base_cdc import BaseCdc


class CdcReferralOutcomes(BaseCdc):

    ART_AlreadyOn = models.CharField(max_length=5, null=True)
    ART_Initiated = models.CharField(max_length=5, null=True)
    ART_Initiated_Date = models.DateField(null=True)
    Age = models.IntegerField(null=True)
    Comments = models.CharField(max_length=250, null=True)
    DOB = models.DateField(null=True)
    Date_Linked = models.DateField(null=True)
    Gender = models.CharField(max_length=5, null=True)
    Referral_Outcome = models.CharField(max_length=100, null=True)
    SSID = models.CharField(max_length=25, null=True)
    Study_Participant_ID = models.CharField(max_length=25, null=True)
    omang = IdentityField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
