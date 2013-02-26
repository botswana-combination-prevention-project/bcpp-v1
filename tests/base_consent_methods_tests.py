from datetime import datetime
from django.db.models import get_model
from django.test import TestCase
from bhp_variables.models import StudySite, StudySpecific
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import TestSubjectConsent
from bhp_consent.exceptions import ConsentError


class BaseConsentMethodsTests(TestCase):

    def setUp(self):
        self.study_site = StudySite.objects.create(site_code='10', site_name='TEST_SITE')

    def test_save(self):
        # create a consent without a user provided identifier
        subject_consent = TestSubjectConsent.objects.create(
            first_name='TEST',
            last_name='TESTER',
            user_provided_subject_identifier=None,
            initials='TT',
            identity='111111111',
            confirm_identity='111111111',
            identity_type='omang',
            dob=datetime(1990, 01, 01),
            is_dob_estimated='No',
            gender='M',
            subject_type='subject',
            consent_datetime=datetime.today(),
            study_site=self.study_site,
            may_store_samples='Yes')
        # assert a new identifier was created
        self.assertIsNotNone(subject_consent.subject_identifier)
        # assert RegisteredSubject was created with this identifier
        self.assertTrue(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier, subject_consent.subject_identifier)
        # create new consent but provide a user identifier
        user_provided_subject_identifier = 'TEST_IDENTIFIER'
        subject_consent = TestSubjectConsent.objects.create(
            first_name='TEST',
            last_name='TESTER',
            user_provided_subject_identifier=user_provided_subject_identifier,
            initials='TT',
            identity='111111112',
            confirm_identity='111111112',
            identity_type='omang',
            dob=datetime(1990, 01, 01),
            is_dob_estimated='No',
            gender='M',
            subject_type='subject',
            consent_datetime=datetime.today(),
            study_site=self.study_site,
            may_store_samples='Yes',
            )
        # assert user provided identifier was used on the consent model
        self.assertEqual(subject_consent.subject_identifier, user_provided_subject_identifier)
        # assert user provided identifier was used on the RegisteresSubject model
        self.assertTrue(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier, subject_consent.subject_identifier)
        # try to change the user provided identifier
        subject_consent.user_provided_subject_identifier = 'ERIK'
        # assert this raises an exception
        self.assertRaises(ConsentError, subject_consent.save)
        # assert subject identifier was not modified
        self.assertEqual(subject_consent.subject_identifier, user_provided_subject_identifier)
        registered_subject = RegisteredSubject.objects.create()
        subject_consent = TestSubjectConsent.objects.create(
            registered_subject=registered_subject,
            first_name='TEST',
            last_name='TESTER',
            user_provided_subject_identifier=None,
            initials='TT',
            identity='111111113',
            confirm_identity='111111113',
            identity_type='omang',
            dob=datetime(1990, 01, 01),
            is_dob_estimated='No',
            gender='M',
            subject_type='subject',
            consent_datetime=datetime.today(),
            study_site=self.study_site,
            may_store_samples='Yes',
            )
