from django.db import models

from edc.core.crypto_fields.fields import EncryptedIdentityField

from .base_cdc import BaseCdc


class CdcSmcOtse(BaseCdc):

    FirstSaveTime = models.DateTimeField(null=True)
    GlobalRecordId = models.CharField(max_length=50, null=True)
    LastSaveTime = models.DateTimeField(null=True)
    UniqueKey = models.IntegerField(null=True)
    identity_value = EncryptedIdentityField(null=True)
    mcVstIDtypeOM = EncryptedIdentityField(null=True)
    mcVstIDtypePBC = EncryptedIdentityField(null=True)
    mcVstInfoAge = models.IntegerField(null=True)
    mcVstInfoApptdt = models.DateField(null=True)
    mcVstInfoDOB = models.DateField(null=True)
    mcVstInfoDOBnoAge = models.IntegerField(null=True)
    mcVstInfoReslt = models.IntegerField(null=True)
    mcVstInfoSourceDate = models.DateField(null=True)
    mcVstInfotestdate = models.DateField(null=True)
    mcVstSID = models.CharField(max_length=25, null=True)
    mcfuAltCdate = models.DateField(null=True)
    mcfuAltCmade = models.IntegerField(null=True)
    mcfuCdate1 = models.DateField(null=True)
    mcfuCdate2 = models.DateField(null=True)
    mcfuCdate3 = models.DateField(null=True)
    mcfuCdate5 = models.DateField(null=True)
    mcfuOutcome1 = models.IntegerField(null=True)
    mcfuOutcome2 = models.IntegerField(null=True)
    mcfuOutcome3 = models.IntegerField(null=True)
    mcfuOutcome5 = models.IntegerField(null=True)
    mcocmc = models.IntegerField(null=True)
    mcocmcdate = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
