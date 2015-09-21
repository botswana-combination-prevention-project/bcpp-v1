from datetime import datetime

from .factories import HivCareAdherenceFactory
from .base_scheduled_model_test_case import BaseScheduledModelTestCase

from bhp066.apps.bcpp_subject.tests.factories import (SubjectVisitFactory, HicEnrollmentFactory, SubjectLocatorFactory,ResidencyMobilityFactory,
                                               HivResultFactory)
from bhp066.apps.bcpp_survey.models import Survey


class TestHivCareAdherence(BaseScheduledModelTestCase):
    
    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()

    def tests_referred_hiv(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        hiv_care_adherence = HivCareAdherenceFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            )
        self.assertIn('HIV', hiv_care_adherence.referral_code_list)
    
    def test_hivcare_adherence_T0(self):
        """ Attempts to create hivcare_adherence for T0 """
        
    
    def test_hivcare_adherence_T1(self):
        """ Attempts to create hivcare_adherence for T1, prepopulating all fields that has yes answers from T0 """
    
