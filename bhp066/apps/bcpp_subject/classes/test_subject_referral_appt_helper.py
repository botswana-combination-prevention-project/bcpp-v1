from datetime import datetime, date, timedelta

from django.test import SimpleTestCase

from .subject_referral_appt_helper import SubjectReferralApptHelper


class TestSubjectReferralApptHelper(SimpleTestCase):
    """Tests given a referral code correctly calculates the next appointment datetime.

    The calculated appointment dates will differ according to the referral code"""

    def test_clinic_type1(self):
        """Assert POS! referred to IDCC on next day if not pregnant"""

        referral_code = 'POS!-LO'
        expected_clinic_type = 'IDCC'
        subject_referral_appt_helper = SubjectReferralApptHelper(referral_code, scheduled_appt_date=None, smc_start_datetime=None)
        self.assertEqual(subject_referral_appt_helper.clinic_type(), expected_clinic_type)
