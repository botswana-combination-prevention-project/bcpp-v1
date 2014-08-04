from django.db import models

from edc.core.crypto_fields.fields import EncryptedCharField

from .base_cdc import BaseCdc


class CdcHtcIntake(BaseCdc):

    _age_in_years = models.IntegerField(null=True)

    permission = models.IntegerField(null=True)

    community_name = models.IntegerField(null=True)

    permanent_resident_ind = models.IntegerField(null=True)

    part_time_resident = models.IntegerField(null=True)

    resident_community = models.IntegerField(null=True)

    have_omang_ind = models.IntegerField(null=True)

    omang_nbr = EncryptedCharField(max_length=150, null=True)

    spouse_of_citizen_ind = models.IntegerField(null=True)

    tac_location = models.IntegerField(null=True)

    prior_hiv_test_record_available = models.IntegerField(null=True)

    hiv_result_in_past_3m_ind = models.IntegerField(null=True)

    tac_consent = models.IntegerField(null=True)

    test_refusal_reason = models.IntegerField(null=True)

    cd4_test_performed_ind = models.IntegerField(null=True)

    referred_for = models.IntegerField(null=True)

    mc_like_to_be_referred = models.IntegerField(null=True)

    mc_no_interest_reason = models.IntegerField(null=True)

    mc_phone_contact_permission = models.IntegerField(null=True)

    mc_family_phone_contact_permissi = models.IntegerField(null=True)

    hh_id = models.CharField(max_length=25, null=True)

    cd4_res = models.IntegerField(null=True)

    permanent_resident_ind2 = models.IntegerField(null=True)

    citizen_ind2 = models.IntegerField(null=True)

    pregnant_ind2 = models.IntegerField(null=True)

    prior_hiv_result = models.IntegerField(null=True)

    ART_documentation_ind = models.IntegerField(null=True)

    hiv_test_result = models.IntegerField(null=True)

    referral_clinic2 = models.IntegerField(null=True)

    mc_like_to_be_referred2 = models.IntegerField(null=True)

    home_visit_permission2 = models.IntegerField(null=True)

    age_calc = models.IntegerField(null=True)

    intv_dt = models.DateField()

    subject_id = models.CharField(max_length=25, null=True)

    gender = models.IntegerField(null=True)

    DOB = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
