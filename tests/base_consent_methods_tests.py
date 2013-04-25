import re
from datetime import datetime
from django.test import TestCase
from bhp_variables.models import StudySpecific, StudySite
from bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from bhp_registration.models import RegisteredSubject
from bhp_base_model.models import TestForeignKey, TestManyToMany
from bhp_consent.models import TestSubjectConsent, TestSubjectUuidModel, ConsentCatalogue, TestSubjectConsentNoRS
from bhp_identifier.exceptions import IdentifierError
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_content_type_map.models import ContentTypeMap
from base_methods import BaseMethods
from bhp_registration.tests.factories import RegisteredSubjectFactory
from factories import TestSubjectConsentFactory, ConsentCatalogueFactory, TestSubjectConsentNoRSFactory


class BaseConsentMethodsTests(TestCase, BaseMethods):

    def setUp(self):
        self.create_study_variables()

    def test_subject_consent_save(self):
        print 'TEST SUBJECT CONSENT WITH KEY TO RS'
        TestSubjectConsent.objects.all().delete()
        RegisteredSubject.objects.all().delete()
        registered_subject = RegisteredSubjectFactory()
        StudySite.objects.all().delete()
        study_site = StudySiteFactory(site_code='20')
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        self.assertTrue(re_pk.match(str(registered_subject.subject_identifier)))

        print 'create a consent without a user provided identifier'
        subject_consent = TestSubjectConsentFactory(study_site=study_site)
        print 'assert a new identifier was created'
        self.assertIsNotNone(subject_consent.subject_identifier)
        print subject_consent.subject_identifier
        print 'assert RegisteredSubject was created or updated with this identifier'
        self.assertTrue(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier, subject_consent.subject_identifier)
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        print 'assert subject_consent registered subject is set with the same registered_subject'
        self.assertEqual(subject_consent.registered_subject.pk, registered_subject.pk)

        print 'create another consent but provide a subject_identifier=\'TEST_IDENTIFIER\''
        user_provided_subject_identifier = 'TEST_IDENTIFIER'
        subject_consent = TestSubjectConsentFactory(user_provided_subject_identifier=user_provided_subject_identifier, study_site=study_site)
        print subject_consent.subject_identifier
        print 'assert provided subject_identifier was used on the consent model'
        self.assertEqual(subject_consent.subject_identifier, user_provided_subject_identifier)
        print 'assert provided subject_identifier was used when creating/updating the RegisteresSubject model'
        self.assertEqual(RegisteredSubject.objects.filter(subject_identifier=subject_consent.subject_identifier).count(), 1)
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        print 'assert subject_consent registered subject is set with the same registered_subject'
        self.assertEqual(subject_consent.registered_subject.pk, registered_subject.pk)
        print 'assert trying to change the user provided identifier raises an exception'
        subject_consent.user_provided_subject_identifier = 'TEST_IDENTIFIER_X'
        self.assertRaises(IdentifierError, subject_consent.save)
        print 'assert subject identifier was not modified'
        self.assertEqual(subject_consent.subject_identifier, user_provided_subject_identifier)

        print 'create a consent, but do not specify registered subject'
        self.assertEqual(RegisteredSubject.objects.all().count(), 3)
        subject_consent = TestSubjectConsentFactory(study_site=study_site)
        print subject_consent.subject_identifier
        print 'assert subject_identifier was created and a registered subject was updated'
        self.assertEqual(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier, subject_consent.subject_identifier)
        self.assertEqual(RegisteredSubject.objects.all().count(), 4)
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        print 'assert subject_consent registered subject is set with the same registered_subject'
        self.assertEqual(subject_consent.registered_subject.pk, registered_subject.pk)

        print 'create a blank RegisteredSubject'
        registered_subject = RegisteredSubject.objects.create()
        print 'create a consent with registered subject'
        subject_consent = TestSubjectConsentFactory(registered_subject=registered_subject, study_site=study_site)
        print subject_consent.subject_identifier
        print 'assert subject_identifier was created and a registered subject was updated'
        self.assertEqual(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier, subject_consent.subject_identifier)
        print 'create a registered subject and set the subject identifier'
        registered_subject = RegisteredSubjectFactory(subject_identifier="REGISTERED_SUBJECT_ID")
        print 'create a consent related to the registerred_subject'
        subject_consent = TestSubjectConsentFactory(registered_subject=registered_subject, study_site=study_site)
        print subject_consent.subject_identifier
        print 'assert the consent used the subject_identifier on registered_subject'
        self.assertEqual(subject_consent.subject_identifier, "REGISTERED_SUBJECT_ID")
        print 'assert the identifier on registered_subject was not changed'
        self.assertEqual(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier, "REGISTERED_SUBJECT_ID")
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        print 'assert subject_consent registered subject is set with the same registered_subject'
        self.assertEqual(subject_consent.registered_subject.pk, registered_subject.pk)
        print 'ok'

    def test_subject_consent_no_registered_subject(self):
        print 'TEST SUBJECT CONSENT WITH NO KEY TO RS'
        TestSubjectConsent.objects.all().delete()
        TestSubjectConsentNoRS.objects.all().delete()
        RegisteredSubject.objects.all().delete()
        print 'create registered subject, assert subject identifier and subject_identifier_as_pk set to dummy pk'
        registered_subject = RegisteredSubjectFactory()
        StudySite.objects.all().delete()
        study_site = StudySiteFactory(site_code='20')
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        self.assertTrue(re_pk.match(str(registered_subject.subject_identifier)))
        self.assertTrue(re_pk.match(str(registered_subject.subject_identifier_as_pk)))

        print 'create a consent without a user provided identifier and no key to RS'
        subject_consent = TestSubjectConsentNoRSFactory(study_site=study_site)
        print 'assert a new identifier was created'
        self.assertIsNotNone(subject_consent.subject_identifier)
        print subject_consent.subject_identifier
        print 'assert RegisteredSubject was created or updated with this identifier'
        self.assertTrue(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier, subject_consent.subject_identifier)
        print 'create another consent but provide a subject_identifier=\'TEST_IDENTIFIER\''
        user_provided_subject_identifier = 'TEST_IDENTIFIER'
        subject_consent = TestSubjectConsentNoRSFactory(user_provided_subject_identifier=user_provided_subject_identifier, study_site=study_site)
        print subject_consent.subject_identifier
        print 'assert provided subject_identifier was used on the consent model'
        self.assertEqual(subject_consent.subject_identifier, user_provided_subject_identifier)
        print 'assert provided subject_identifier was used when creating/updating the RegisteresSubject model'
        self.assertEqual(RegisteredSubject.objects.filter(subject_identifier=subject_consent.subject_identifier).count(), 1)
        print 'assert trying to change the user provided identifier raises an exception'
        subject_consent.user_provided_subject_identifier = 'TEST_IDENTIFIER_X'
        self.assertRaises(IdentifierError, subject_consent.save)
        print 'assert subject identifier was not modified'
        self.assertEqual(subject_consent.subject_identifier, user_provided_subject_identifier)
        print 'create another consent without RS key'
        self.assertEqual(RegisteredSubject.objects.all().count(), 3)
        subject_consent = TestSubjectConsentNoRSFactory(study_site=study_site)
        print subject_consent.subject_identifier
        print 'assert subject_identifier was created and a registered subject was created for this consent'
        self.assertEqual(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier, subject_consent.subject_identifier)
        print 'assert subject_identifier_pk is same on registered subject and this consent'
        self.assertEqual(RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier).subject_identifier_as_pk, subject_consent.subject_identifier_as_pk)

        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier, identity=subject_consent.identity)
        print 'assert registered_subject fields were updated from BaseSubject fields in subject_consent'
        self.assertEqual(registered_subject.first_name, subject_consent.first_name)
        self.assertEqual(registered_subject.last_name, subject_consent.last_name)
        self.assertEqual(registered_subject.identity_type, subject_consent.identity_type)
        #self.assertEqual(registered_subject.study_site.site_code, subject_consent.study_site.site_code)
        self.assertEqual(registered_subject.gender, subject_consent.gender)
        self.assertEqual(registered_subject.initials, subject_consent.initials)
        self.assertEqual(registered_subject.dob, subject_consent.dob)
        self.assertEqual(registered_subject.is_dob_estimated, subject_consent.is_dob_estimated)
        self.assertEqual(registered_subject.subject_identifier_as_pk, subject_consent.subject_identifier_as_pk)
        self.assertEqual(RegisteredSubject.objects.all().count(), 4)
        print 'ok'

    def test_consent_catalogue(self):
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        # prepare the consent catalogue
        content_type_map = ContentTypeMap.objects.get(model__iexact=TestSubjectConsent._meta.object_name)
        ConsentCatalogueFactory(content_type_map=content_type_map, add_for_app='bhp_consent')

    def test_subject_uuid_model(self):
        self.test_consent_catalogue()
        test_m2m2 = TestManyToMany.objects.create(name='test_m2m2', short_name='test_m2m2')
        TestManyToMany.objects.create(name='test_m2m3', short_name='test_m2m3')
        TestForeignKey.objects.create(name='test_fk', short_name='test_fk')
        registered_subject = RegisteredSubject.objects.create(subject_identifier="TEST_SUBJECT_UUID")
        TestSubjectConsent.objects.create(
            registered_subject=registered_subject,
            first_name='TEST_SUBJECT_UUID',
            last_name='TEST_SUBJECT_UUIDER',
            user_provided_subject_identifier=None,
            initials='TT',
            identity='111111115',
            confirm_identity='111111115',
            identity_type='omang',
            dob=datetime(1990, 01, 01),
            is_dob_estimated='No',
            gender='M',
            subject_type='subject',
            consent_datetime=datetime.today(),
            study_site=self.study_site,
            may_store_samples='Yes',
            )
        test_subject_uuid_model = TestSubjectUuidModel(
            name='TEST',
            registered_subject=registered_subject,
            test_foreign_key=TestForeignKey.objects.all()[0],
            )
        test_subject_uuid_model.save()
        test_subject_uuid_model.test_many_to_many.add(test_m2m2)
        test_subject_uuid_model = TestSubjectUuidModel.objects.get(pk=test_subject_uuid_model.pk)
        self.assertEqual([m2m.name for m2m in test_subject_uuid_model.test_many_to_many.all()], [test_m2m2.name])
