from django.core import serializers
from django.db.models import get_app, get_models
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.core.crypto_fields.classes import FieldCryptor
from edc.device.sync.classes import SerializeToTransaction
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.appointment.models import Appointment
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_clinic_enrollment.tests.factories import ClinicEligibilityFactory, ClinicEnrollmentLossFactory
from apps.bcpp_clinic.tests.factories import (ClinicConsentFactory, ClinicVisitFactory,
                                             ClinicLocatorFactory, ClinicQuestionnaireFactory)
from apps.bcpp_clinic_enrollment.models import ClinicEnrollmentLoss
from apps.clinic.bcpp_clinic_configuration.classes import BcppClinicConfiguration
from apps.bcpp_clinic.visit_schedule import BcppClinicVisitSchedule
from apps.bcpp_clinic_lab.lab_profiles import ClinicSubjectProfile


class NaturalKeyTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(ClinicSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppClinicConfiguration()
        site_lab_tracker.autodiscover()
        BcppClinicVisitSchedule().build()

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
        RegisteredSubject.objects.all().delete()
        instances = []
        self.assertEqual(ClinicEnrollmentLoss.objects.all().count(), 0)
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        clinic_eligibility = ClinicEligibilityFactory()
        subjects = RegisteredSubject.objects.all()
        self.assertTrue(clinic_eligibility.is_eligible)
        clinic_eligibility.legal_marriage = 'No'
        clinic_eligibility.save()
        self.assertFalse(clinic_eligibility.is_eligible)
        self.assertEqual(ClinicEnrollmentLoss.objects.all().count(), 1)
        clinic_loss = ClinicEnrollmentLoss.objects.all()[0]
        instances.append(clinic_loss)
        clinic_eligibility.legal_marriage = 'Yes'
        clinic_eligibility.save()
        self.assertTrue(clinic_eligibility.is_eligible)
        instances.append(clinic_eligibility)

        clinic_consent = ClinicConsentFactory(dob=clinic_eligibility.dob,
                                              gender=clinic_eligibility.gender,
                                              first_name=clinic_eligibility.first_name,
                                              initials=clinic_eligibility.initials)
        self.assertEqual(Appointment.objects.all().count(), 1)
        instances.append(clinic_consent)
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        registered_subject = RegisteredSubject.objects.get(dob=clinic_eligibility.dob,
                                              gender=clinic_eligibility.gender,
                                              first_name=clinic_eligibility.first_name,
                                              initials=clinic_eligibility.initials)

        appointment = Appointment.objects.get(registered_subject = registered_subject)
        clinic_visit = ClinicVisitFactory(appointment = appointment)
        instances.append(clinic_visit)
        clinic_subject_locator = ClinicLocatorFactory(clinic_visit = clinic_visit)
        instances.append(clinic_subject_locator)
        clinic_questionnaire = ClinicQuestionnaireFactory(clinic_visit = clinic_visit)
        instances.append(clinic_questionnaire)

        print 'INSTANCE: ' + str(instances)
        for obj in instances:
            print 'test natural key on {0}'.format(obj._meta.object_name)
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        #pp = pprint.PrettyPrinter(indent=4)
        for obj in instances:
            print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj)
            #print repr(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
