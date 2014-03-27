from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db.models import get_app, get_models
from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.core.crypto_fields.classes import FieldCryptor
from edc.device.sync.classes import SerializeToTransaction
from edc.subject.appointment.tests.factories import AppointmentFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from apps.bcpp_survey.models import Survey
from .factories import ClinicConsentFactory, ClinicEligibilityFactory, ClinicVisitFactory


class NaturalKeyTests(TestCase):

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_clinic')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_clinic')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        site_lab_tracker.autodiscover()
        StudySpecificFactory()
        study_site = StudySiteFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        print 'setup the consent catalogue for this BCPP'
        content_type_map = ContentTypeMap.objects.get(content_type__model__iexact='ClinicConsent')
        print ContentTypeMap.objects.all().count()
        consent_catalogue = ConsentCatalogueFactory(name='bcpp year 0', content_type_map=content_type_map)
        consent_catalogue.add_for_app = 'bcpp_clinic'
        consent_catalogue.save()
        clinic_visit_content_type = ContentType.objects.get(app_label='bcpp_clinic', model='clinicvisit')
        clinic_visit_content_type_map = ContentTypeMap.objects.get(content_type=clinic_visit_content_type)
        from edc.subject.visit_schedule.tests.factories import VisitDefinitionFactory
        visit_definition = VisitDefinitionFactory(visit_tracking_content_type_map=clinic_visit_content_type_map)

        # SubjectConsentFactory = get_model('bcpp_subject','SubjectConsentFactory')
        survey1 = Survey.objects.create(survey_name='YEAR 0',
                          datetime_start=datetime.today() - timedelta(days=30),
                          datetime_end=datetime.today() + timedelta(days=180)
                          )
#         print 'Clear previous Registered Subjects: Count='+str(RegisteredSubject.objects.all().count())
#         RegisteredSubject.objects.all().delete()

        subject_clinic_consent = ClinicConsentFactory()

        #registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        registered_subject = subject_clinic_consent.registered_subject
        instances = []
        instances.append(subject_clinic_consent)
        instances.append(registered_subject)

        clinic_eligiility = ClinicEligibilityFactory(registered_subject=registered_subject)
        instances.append(clinic_eligiility)
        appointment = AppointmentFactory(registered_subject=registered_subject, visit_definition=visit_definition)
        clinic_visit = ClinicVisitFactory(appointment=appointment)
        instances.append(clinic_visit)
        #clinic_off_study = ClinicOffStudyFactory()
        #instances.append(clinic_off_study)

        print 'INSTANCE: ' + str(instances)
        for obj in instances:
            print 'test natural key on {0}'.format(obj._meta.object_name)
            natural_key = obj.natural_key()
            print 'getting '+str(obj.__class__)
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        # pp = pprint.PrettyPrinter(indent=4)
        for obj in instances:
            print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj)
            # pp.pprint(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
