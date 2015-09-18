from django.db import models

from edc_base.encrypted_fields import IdentityField
from .base_cdc import BaseCdc


class CdcHtcIntake(BaseCdc):
    """Aug 30 format"""
    ART_documentation_ind = models.IntegerField(null=True)
    DOB = models.DateField(null=True)
    Prior_HIV_Test_Date = models.DateField(null=True)  # new
    age_calc = models.IntegerField(null=True)
    cd4_res = models.IntegerField(null=True)
    cd4_test_performed_ind = models.IntegerField(null=True)
    citizen_ind = models.IntegerField(null=True)
    community_name = models.IntegerField(null=True)
    form_version = models.CharField(max_length=50, null=True)
    gender = models.IntegerField(null=True)
    have_omang_ind = models.IntegerField(null=True)
    have_passport = models.IntegerField(null=True)
    hh_id = models.CharField(max_length=25, null=True)
    hiv_result_in_past_3m_ind = models.IntegerField(null=True)
    hiv_test_result = models.IntegerField(null=True)
    home_visit_permission = models.IntegerField(null=True)
    intv_dt = models.DateField(null=True)
    mc_family_phone_contact_permissi = models.IntegerField(null=True)
    mc_like_to_be_referred = models.IntegerField(null=True)
    # mc_like_to_be_referred2 = models.IntegerField(null=True)
    mc_no_interest_reason = models.CharField(max_length=50, null=True)
    mc_phone_contact_permission = models.IntegerField(null=True)
    MC_tent_appointment_Date = models.DateField(null=True)
    omang_pass_nbr = IdentityField(max_length=78, null=True)
    # omang_nbr = EncryptedIdentityField(max_length=25, null=True)
    part_time_resident = models.IntegerField(null=True)
    permanent_resident_ind = models.IntegerField(null=True)
    # permanent_resident_ind2 = models.IntegerField(null=True)
    permission = models.IntegerField(null=True)
    pregnant_ind = models.IntegerField(null=True)
    prior_hiv_result = models.IntegerField(null=True)
    prior_hiv_test_record_available = models.IntegerField(null=True)
    referral_clinic = models.CharField(max_length=25, null=True)
    referred_for = models.CharField(max_length=25, null=True)
    resident_community = models.CharField(max_length=50, null=True)
    spouse_of_citizen_ind = models.IntegerField(null=True)
    subject_id = models.CharField(max_length=25, null=True)
    tac_consent = models.IntegerField(null=True)
    tac_location = models.IntegerField(null=True)
    test_refusal_reason = models.IntegerField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
