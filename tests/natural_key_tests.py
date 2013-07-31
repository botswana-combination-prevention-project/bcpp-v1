import pprint
from django.test import TestCase
from django.core import serializers
from bhp_crypto.classes import FieldCryptor

from django.db.models import get_app, get_models
from bhp_lab_tracker.classes import lab_tracker
from bhp_sync.classes import SerializeToTransaction
from bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from bhp_registration.models import RegisteredSubject
from bhp_consent.tests.factories import ConsentCatalogueFactory
from bhp_appointment.models import Appointment
from bhp_appointment.tests.factories import ConfigurationFactory
from bhp_visit.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_content_type_map.models import ContentTypeMap
from bcpp_subject.tests.factories import SubjectConsentFactory
from bcpp_subject.tests.factories import SubjectVisitFactory

class NaturalKeyTests(TestCase):

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_subject')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_subject')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        lab_tracker.autodiscover()
        StudySpecificFactory()
        study_site = StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        print 'setup the consent catalogue for this BCPP'
        content_type_map = ContentTypeMap.objects.get(content_type__model__iexact='SubjectConsent')
        consent_catalogue = ConsentCatalogueFactory(name='bcpp year 0', content_type_map=content_type_map)
        consent_catalogue.add_for_app = 'bcpp_subject'
        consent_catalogue.save()

        print 'consent the subject'
        subject_consent = SubjectConsentFactory(study_site=study_site)
        print subject_consent.subject_identifier
        print 'get registered subject'
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        instances = []
        instances.append(subject_consent)
        instances.append(registered_subject)

        print 'test natural key / get_by_natural_key on subject_visit'
        appointment = Appointment.objects.get(registered_subject=registered_subject, visit_definition__code='1000')
        subject_visit = SubjectVisitFactory(appointment=appointment)
        instances.append(subject_visit)

        for obj in instances:
            print 'test natural key on {0}'.format(obj._meta.object_name)
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        pp = pprint.PrettyPrinter(indent=4)
        for obj in instances:
            print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj)
            #pp.pprint(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
