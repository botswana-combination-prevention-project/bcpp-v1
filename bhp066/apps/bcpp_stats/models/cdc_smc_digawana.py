from django.db import models

from edc.core.crypto_fields.fields import EncryptedCharField

from .base_cdc import BaseCdc


class CdcSmcDigawana(BaseCdc):

    SMC_Followup_UID = models.IntegerField(null=True)

    subject_identifier = models.CharField(max_length=25, null=True)

    identity_type = models.CharField(max_length=25, null=True)

    identity_Value = EncryptedCharField(max_length=150, null=True)

    Source_System_Name = models.CharField(max_length=25, null=True)

    Age = models.IntegerField(null=True)

    Visit_datetime = models.DateTimeField(null=True)

    hiv_result = models.CharField(max_length=25, null=True)

    referral_appt_date = models.DateField(null=True)

    Contact1_DTM = models.DateTimeField(null=True)

    Contact1_Made = models.CharField(max_length=25, null=True)

    Contact2_DTM = models.DateTimeField(null=True)

    Contact2_Made = models.CharField(max_length=25, null=True)

    Contact3_DTM = models.DateTimeField(null=True)

    Contact3_Made = models.CharField(max_length=25, null=True)

    Alt_Contact_DTM = models.DateTimeField(null=True)

    Alt_Contact_Made = models.CharField(max_length=25, null=True)

    Had_MC = models.CharField(max_length=25, null=True)

    MC_Date = models.DateTimeField(null=True)

    subject_ID = models.CharField(max_length=25, null=True)

    Visit_datetime_x = models.DateTimeField(null=True)

    age_cal = models.IntegerField(null=True)

    Contact1_DTM_x = models.DateTimeField(null=True)

    Contact2_DTM_x = models.DateTimeField(null=True)

    MC_Date_x = models.DateTimeField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
