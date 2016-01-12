from datetime import datetime, date
from dateutil.relativedelta import MO, TU, WE, TH, FR

from django.test import TestCase

from ..classes import SubjectReferralApptHelper
from bhp066.apps.bcpp_household.utils.clinic_days_tuple import ClinicDaysTuple

CLINIC_DAYS = {
    '96': {'IDCC': ClinicDaysTuple((MO, ), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2014, 11, 24))},
    '97': {'IDCC': ClinicDaysTuple((MO, ), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2014, 11, 24))},
    '98': {'IDCC': ClinicDaysTuple((MO, WE), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2014, 11, 24))},
    '99': {'IDCC': ClinicDaysTuple((MO, WE), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((WE, ), date(2014, 11, 15))}}


class TestSubjectReferralApptHelper(TestCase):
    """Tests given a referral code correctly calculates the next appointment datetime.

    The calculated appointment dates will differ according to the referral code"""

    def test_masa1(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""
        expected_appt_day = 'Mon'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 9, 8, 7, 30, 0)
        community_code = '97'
        referral_code = 'MASA-CC'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(
            referral_appt_datetime, expected_appt_datetime,
            'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa1a(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""

        expected_appt_day = 'Mon'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 9, 8, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-CC'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(
            referral_appt_datetime, expected_appt_datetime,
            'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa1b(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""

        expected_appt_day = 'Mon'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 9, 8, 7, 30, 0)
        community_code = '96'
        referral_code = 'MASA-CC'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(
            referral_appt_datetime, expected_appt_datetime,
            'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa1c(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""
        expected_appt_day = 'Mon'
        today = date(2015, 2, 13)
        expected_appt_datetime = datetime(2015, 2, 23, 7, 30, 0)
        community_code = '97'
        referral_code = 'MASA-CC'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(
            referral_appt_datetime, expected_appt_datetime,
            'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa2(self):
        """Assert give next clinic day MASA client at the IDCC that is a suspected defaulter with no appointment"""

        expected_appt_day = 'Wed'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 8, 27, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-DF'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(
            referral_appt_datetime,
            expected_appt_datetime,
            'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa2a(self):
        """Assert give next clinic day MASA client at the IDCC that is a suspected defaulter with an appointment"""

        expected_appt_day = 'Wed'
        today = date(2014, 8, 25)
        scheduled_appt_date = date(2014, 9, 17)
        expected_appt_datetime = datetime(2014, 8, 27, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-DF'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(
            referral_appt_datetime,
            expected_appt_datetime,
            'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa3(self):
        """Assert give next clinic day in 3 weels for a MASA client at the IDCC with a scheduled appt in 3 weeks"""
        expected_appt_day = 'Wed'
        today = date(2014, 8, 26)
        scheduled_appt_date = date(2014, 9, 17)
        expected_appt_datetime = datetime(2014, 9, 17, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-CC'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa4(self):
        """Assert give next clinic day in two weeks for a MASA client at the IDCC with a scheduled appt in 2 weeks"""
        expected_appt_day = 'Wed'
        today = date(2014, 8, 26)
        scheduled_appt_date = datetime(2014, 9, 9, 7, 30, 0)
        expected_appt_datetime = datetime(2014, 9, 10, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-CC'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa5(self):
        """Assert give two week appointment if scheduled appt is more than a month away."""
        expected_appt_day = 'Mon'
        today = date(2014, 8, 26)
        scheduled_appt_date = datetime(2014, 9, 29, 7, 30, 0)
        expected_appt_datetime = datetime(2014, 9, 8, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-CC'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc1(self):
        """Assert referred on smc_start date for SMC subjected seen on a date before the smc start date"""
        expected_appt_day = 'Mon'
        today = date(2014, 8, 30)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 24, 7, 30, 0)
        community_code = '98'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc1a(self):
        """Assert referred on ECC smc_start date for SMC subjected seen on a date before
        the smc start date (start date is SAT)"""
        expected_appt_day = 'Wed'
        today = date(2014, 8, 30)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 19, 7, 30, 0)
        community_code = '99'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc2(self):
        """Assert referred on on smc day for SMC subjected seen on a date AFTER the smc start date (TU->WE)"""
        expected_appt_day = 'Mon'
        today = date(2014, 11, 28)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 12, 1, 7, 30, 0)
        community_code = '98'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc3(self):
        """Assert referred on on smc day for SMC subjected seen on a date AFTER the smc start date (SA->MO)"""
        expected_appt_day = 'Mon'
        today = date(2014, 11, 29)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 12, 1, 7, 30, 0)
        community_code = '98'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv1(self):
        """Assert referred to VCT testing"""
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'TST-HIV'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv2(self):
        """Assert referred POS#-HI to IDCC testing"""
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS#-HI'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv3(self):
        """Assert referred POS#-HI to IDCC testing"""
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS#-LO'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv4(self):
        """Assert referred POS#-HI to IDCC testing"""
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS!-LO'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv5(self):
        """Assert referred POS#-HI to IDCC testing"""
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS!-HI'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_POS_next_clinic_day(self):
        """Test that POS! will get the next clinic date"""

        expected_appt_day = 'Wed'
        today = date(2015, 3, 2)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2015, 3, 4, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS!-HI'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))
        # Test with only 1 IDCC day.
        expected_appt_day = 'Mon'
        expected_appt_datetime = datetime(2015, 3, 9, 7, 30, 0)
        community_code = '96'
        referral_code = 'POS!-HI'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime,
                                             subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))
