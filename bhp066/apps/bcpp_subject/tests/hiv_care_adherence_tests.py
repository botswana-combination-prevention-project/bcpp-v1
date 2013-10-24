from datetime import datetime

from .factories import HivCareAdherenceFactory
from .base_scheduled_model_test_case import BaseScheduledModelTestCase


class HivCareAdherenceTests(BaseScheduledModelTestCase):

    def tests_referred_hiv(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        hiv_care_adherence = HivCareAdherenceFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            )
        self.assertIn('HIV', hiv_care_adherence.referral_code_list)
