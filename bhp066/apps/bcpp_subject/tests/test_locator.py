from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.utils import override_settings
from edc_constants.constants import YES, NO
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from ..models import SubjectLocator
from bhp066.apps.bcpp_subject.tests.factories._subject_visit_factory import SubjectVisitFactory
from edc.subject.appointment.tests.factories.appointment_factory import AppointmentFactory
from bhp066.apps.bcpp_subject.tests.factories.hic_enrollment_factory import HicEnrollmentFactory
from bhp066.apps.bcpp_subject.tests.factories.subject_locator_factory import SubjectLocatorFactory
from edc.subject.appointment.models.appointment import Appointment
from edc.apps.app_configuration.models.global_configuration import GlobalConfiguration
from edc.core.bhp_content_type_map.models.content_type_map import ContentTypeMap
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp.app_configuration.classes.app_configuration import BcppAppConfiguration
from edc.subject.lab_tracker.classes.controller import site_lab_tracker
from bhp066.apps.bcpp_subject.visit_schedule.bcpp_subject import BcppSubjectVisitSchedule
from edc.subject.rule_groups.classes.controller import site_rule_groups
from bhp066.apps.bcpp_survey.tests.factories.survey_factory import SurveyFactory
from edc.lab.lab_profile.classes.controller import site_lab_profiles
from bhp066.apps.bcpp_subject.tests.base_rule_group_test_setup import BaseRuleGroupTestSetup


class TestLocator(BaseRuleGroupTestSetup):

    @override_settings(VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER=False)
    def setUp(self):
        super(TestLocator, self).setUp()
#         try:
#             site_lab_profiles.register(BcppSubjectProfile())
#         except AlreadyRegisteredLabProfile:
#             pass
#         BcppAppConfiguration().prepare()
#         site_lab_tracker.autodiscover()
#         BcppSubjectVisitSchedule().build()
#         site_rule_groups.autodiscover()
#         SurveyFactory()
#         self.appointment = AppointmentFactory()
#         self.subject_visit = SubjectVisitFactory(appointment=self.appointment)

    def test_locator_may_follow_up(self):
        self.locator = SubjectLocatorFactory(may_follow_up=YES, subject_visit=self.subject_visit)
        self.enrollment = HicEnrollmentFactory(subject_visit=self.subject_visit)
        self.locator.subject_cell = '71717788'
        self.locator.save()
        self.assertEqual(SubjectLocator.objects.get(subject_visit=self.subject_visit).subject_cell, '71717788')

    def test_locator_may_follow_up1(self):
        locator = SubjectLocatorFactory(may_follow_up=YES, may_sms_follow_up=YES, subject_visit=self.subject_visit, subject_cell='')
        with self.assertRaises(ValidationError):
            locator.full_clean()

    def test_locator_may_follow_up2(self):
        locator = SubjectLocatorFactory(may_follow_up=NO, may_sms_follow_up=YES, subject_visit=self.subject_visit, subject_cell='')
        with self.assertRaises(ValidationError):
            locator.full_clean()

    def test_locator_may_follow_up3(self):
        locator = SubjectLocatorFactory(may_follow_up=YES, may_sms_follow_up=NO, subject_visit=self.subject_visit, subject_cell='')
        with self.assertRaises(ValidationError):
            locator.full_clean()

    def test_locator_may_follow_up4(self):
        locator = SubjectLocatorFactory(may_follow_up=NO, may_sms_follow_up=NO, subject_visit=self.subject_visit, subject_cell='')
        HicEnrollmentFactory(subject_visit=self.subject_visit)
        locator.subject_cell = '71717788'
        with self.assertRaises(ValidationError):
            locator.full_clean()
