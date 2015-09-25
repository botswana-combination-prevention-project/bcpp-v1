from django.core.exceptions import ValidationError
from django.test import TestCase
from edc.choices.common import YES, NO

from ..models import SubjectLocator
from bhp066.apps.bcpp_subject.tests.factories._subject_visit_factory import SubjectVisitFactory
from edc.subject.appointment.tests.factories.appointment_factory import AppointmentFactory
from bhp066.apps.bcpp_subject.tests.factories.hic_enrollment_factory import HicEnrollmentFactory
from bhp066.apps.bcpp_subject.tests.factories.subject_locator_factory import SubjectLocatorFactory


class TestLocator(TestCase):

    def setUp(self):
        self.appointment = AppointmentFactory()
        self.subject_visit = SubjectVisitFactory(appointment=self.appointment)

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
