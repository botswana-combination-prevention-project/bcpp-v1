from django.db import models

from edc_base.encrypted_fields import IdentityField
from .base_cdc import BaseCdc


class CdcHtcIntakeForClinic(BaseCdc):

    community_name = models.IntegerField(null=True)
    omang_nbr = IdentityField(null=True)
    pregnant_ind = models.IntegerField(null=True)
    prior_hiv_result = models.IntegerField(null=True)
    prior_hiv_test_date = models.DateField(null=True)
    prior_hiv_test_record_available = models.IntegerField(null=True)
    referral_appt_datetime = models.DateField(null=True)
    referred_for = models.CharField(max_length=25, null=True)
    referred_for_desc = models.CharField(max_length=250, null=True)
    subject_id = models.CharField(max_length=25, null=True)
    subject_id_reformatted = models.CharField(max_length=25, null=True)

    class Meta:
        app_label = 'bcpp_stats'
