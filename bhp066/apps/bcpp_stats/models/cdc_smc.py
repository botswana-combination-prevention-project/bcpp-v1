from django.db import models

from edc.core.crypto_fields.fields import EncryptedCharField

from .base_cdc import BaseCdc


class CdcSmc(BaseCdc):

    _age_in_years = models.IntegerField(null=True)

    UniqueKey = models.CharField(max_length=150, null=True)

    mcVstSID = models.CharField(max_length=150, null=True)

    mcVstIDtypeOM = EncryptedCharField(max_length=150, null=True)

    mcVstIDtypePBC = EncryptedCharField(max_length=150, null=True)

    mcVstInfoSourceDate = models.DateField(null=True)

    mcVstInfoDOB = models.DateTimeField(null=True)

    mcVstInfoAge = models.CharField(max_length=150, null=True)

    mcVstInfoDOBnoAge = models.CharField(max_length=150, null=True)

    mcVstInfotestdateNo = models.IntegerField(null=True)

    mcVstInfoApptdt = models.DateField(null=True)

    mcVstInfoReslt = models.CharField(max_length=150, null=True)

    mcfuCdate1 = models.DateField(null=True)

    mcfuCdate2 = models.DateField(null=True)

    mcfuCdate3 = models.DateField(null=True)

    mcfuAltCdate = models.DateField(null=True)

    mcfuAltCmade = models.CharField(max_length=150, null=True)

    mcfuOutcome1 = models.CharField(max_length=150, null=True)

    mcfuOutcome2 = models.CharField(max_length=150, null=True)

    mcfuOutcome3 = models.CharField(max_length=150, null=True)

    mcocmc = models.CharField(max_length=150, null=True)

    mcocmcdate = models.DateField(null=True)

    hiv_result = models.CharField(max_length=150, null=True)

    hiv_result_datetime = models.DateTimeField(null=True)

    last_hiv_result = models.CharField(max_length=150, null=True)

    last_hiv_test_date = models.DateTimeField(null=True)

    referral_code = models.CharField(max_length=150, null=True)

    class Meta:
        app_label = 'bcpp_stats'
