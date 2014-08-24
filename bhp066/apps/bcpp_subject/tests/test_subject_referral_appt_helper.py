from datetime import datetime, date, timedelta
from dateutil.relativedelta import MO, TU, WE, TH, FR

from django.test import SimpleTestCase

from ..classes import SubjectReferralApptHelper

CLINIC_DAYS = {
    '11': {'IDCC': ((MO, WE), ), 'ANC': ((MO, TU, WE, TH, FR), ), 'SMC': ((MO, TU, WE, TH, FR), date(2014, 10, 15)), 'SMC-ECC': ((MO, TU, WE, TH, FR), date(2014, 10, 7))},
    '12': {'IDCC': ((MO, WE), ), 'ANC': ((MO, TU, WE, TH, FR), ), 'SMC': ((MO, TU, WE, TH, FR), date(2014, 10, 15)), 'SMC-ECC': ((MO, TU, WE, TH, FR), date(2014, 10, 7))},
    }


class TestSubjectReferralApptHelper(SimpleTestCase):
    """Tests given a referral code correctly calculates the next appointment datetime.

    The calculated appointment dates will differ according to the referral code"""

    def test_masa1(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""
        today_day = 'Mon'
        expected_appt_day = 'Mon'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 9, 8, 7, 30, 0)
        community_code = '11'
        referral_code = 'MASA-CC'
        subject_referral_appt_helper = SubjectReferralApptHelper(community_code, referral_code)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa2(self):
        """Assert give next clinic day MASA client at the IDCC that is a suspected defaulter with no appointment"""
        today_day = 'Mon'
        expected_appt_day = 'Wed'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 8, 27, 7, 30, 0)
        community_code = '11'
        referral_code = 'MASA-DF'
        subject_referral_appt_helper = SubjectReferralApptHelper(community_code, referral_code, today)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa2a(self):
        """Assert give next clinic day MASA client at the IDCC that is a suspected defaulter with an appointment"""
        today_day = 'Mon'
        expected_appt_day = 'Wed'
        today = date(2014, 8, 25)
        scheduled_appt_date = date(2014, 9, 17)
        expected_appt_datetime = datetime(2014, 8, 27, 7, 30, 0)
        community_code = '11'
        referral_code = 'MASA-DF'
        subject_referral_appt_helper = SubjectReferralApptHelper(community_code, referral_code, today, scheduled_appt_date)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa3(self):
        """Assert give next clinic day in 3 weels for a MASA client at the IDCC with a scheduled appt in 3 weeks"""
        today_day = 'Tue'
        expected_appt_day = 'Wed'
        today = date(2014, 8, 26)
        scheduled_appt_date = date(2014, 9, 17)
        expected_appt_datetime = datetime(2014, 9, 17, 7, 30, 0)
        community_code = '11'
        referral_code = 'MASA-CC'
        subject_referral_appt_helper = SubjectReferralApptHelper(community_code, referral_code, today, scheduled_appt_date)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa4(self):
        """Assert give next clinic day in two weeks for a MASA client at the IDCC with a scheduled appt in 2 weeks"""
        today_day = 'Tue'
        expected_appt_day = 'Wed'
        today = date(2014, 8, 26)
        scheduled_appt_date = datetime(2014, 9, 9, 7, 30, 0)
        expected_appt_datetime = datetime(2014, 9, 10, 7, 30, 0)
        community_code = '11'
        referral_code = 'MASA-CC'
        subject_referral_appt_helper = SubjectReferralApptHelper(community_code, referral_code, today, scheduled_appt_date)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc1(self):
        """Assert referred on smc_start date for SMC subjected seen on a date before the smc start date"""
        today_day = 'Sat'
        expected_appt_day = 'Wed'
        today = date(2014, 8, 30)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 10, 15, 7, 30, 0)
        community_code = '11'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(community_code, referral_code, today, scheduled_appt_date)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc2(self):
        """Assert referred on on smc day for SMC subjected seen on a date AFTER the smc start date (TU->WE)"""
        today_day = 'Tue'
        expected_appt_day = 'Wed'
        today = date(2014, 10, 28)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 10, 29, 7, 30, 0)
        community_code = '11'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(community_code, referral_code, today, scheduled_appt_date)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc3(self):
        """Assert referred on on smc day for SMC subjected seen on a date AFTER the smc start date (SA->MO)"""
        today_day = 'Sat'
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '11'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(community_code, referral_code, today, scheduled_appt_date)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))
