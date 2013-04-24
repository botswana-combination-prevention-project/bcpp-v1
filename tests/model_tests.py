import re
from django.test import TestCase
from django.conf import settings
from bhp_consent.models import ConsentCatalogue
from bhp_consent.tests.factories import ConsentCatalogueFactory, TestSubjectConsentFactory
from bhp_variables.tests.factories import StudySiteFactory, StudySpecificFactory
from bhp_registration.models import RegisteredSubject


class ModelTests(TestCase):

    def test_p1(self):
        for cls, cls_factory in [(ConsentCatalogue, ConsentCatalogueFactory)]:
            print 'using {0}'.format(cls._meta.object_name)
            print 'test {0} natural key'.format(cls._meta.object_name)
            rs1 = cls_factory()
            args = rs1.natural_key()
            rs2 = cls.objects.get_by_natural_key(*args)
            self.assertEqual(rs1, rs2)

    def test_p2(self):
        """TEST registered subject is create when consent is created"""
        study_site = StudySiteFactory(site_code='10', site_name='TEST_SITE')
        study_specific = StudySpecificFactory()
        print "create a new consent"
        subject_consent = TestSubjectConsentFactory(first_name='ERIK1', study_site=study_site)
        print 'assert subject_identifier is not None. Got {0}'.format(subject_consent.subject_identifier)
        self.assertIsNotNone(subject_consent.subject_identifier)
        # confirm registered_subject is created and updated
        print 'get the registered subject created by the bhp_subject signal.'
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        print 'assert has same subject identifier'
        self.assertEqual(registered_subject.subject_identifier, subject_consent.subject_identifier)
        print 'assert has same first name'
        self.assertEqual(registered_subject.first_name, subject_consent.first_name)
        print "update subject consent, change first name"
        subject_consent.first_name = 'ERIK2'
        subject_consent.save()
        print "confirm registered subject is updated with new first name"
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        self.assertEqual(registered_subject.first_name, 'ERIK2')