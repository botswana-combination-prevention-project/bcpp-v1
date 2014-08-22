from datetime import datetime, date, timedelta

from django.test import SimpleTestCase


class TestSubjectReferralApptHelper(SimpleTestCase):

    community = 'test_community82'

    def test_idcc(self):
        """Assert POS! referred to IDCC on next day if not pregnant"""
        referral_code = 'POS!-LO'
