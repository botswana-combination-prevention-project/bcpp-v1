from datetime import datetime
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

from apps.bcpp_subject.tests.factories import (SubjectConsentFactory, SubjectVisitFactory)
from apps.bcpp_household_member.tests.factories import EnrollmentChecklistFactory
from apps.bcpp_lab.tests.factories import (SubjectRequisitionFactory, ProcessingFactory, PackingListFactory)
from apps.bcpp_lab.models import Aliquot, Panel, AliquotProfile, PackingListItem
from apps.clinic.bcpp_clinic_configuration.classes import BcppClinicConfiguration
from apps.bcpp_clinic.visit_schedule import BcppClinicVisitSchedule
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile


class NaturalKeyTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppClinicConfiguration()
        site_lab_tracker.autodiscover()
        BcppClinicVisitSchedule().build()

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_clinic_lab')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_clinic_lab')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        instances = []
        enrollment_checklist = EnrollmentChecklistFactory()
        self.assertTrue(enrollment_checklist.is_eligible)
        instances.append(enrollment_checklist)
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        registered_subject = RegisteredSubject.objects.all()[0]

        subject_consent = SubjectConsentFactory(dob=enrollment_checklist.dob,
                                              gender=enrollment_checklist.gender,
                                              first_name=enrollment_checklist.first_name,
                                              initials=enrollment_checklist.initials)
        instances.append(subject_consent)
        self.assertEqual(Appointment.objects.all().count(), 1)
        appointment = Appointment.objects.get(registered_subject = registered_subject)
        subject_visit = SubjectVisitFactory(appointment = appointment)
        instances.append(subject_visit)
        panel = Panel.objects.all()[0]
        subjects_requisition = SubjectRequisitionFactory(clinic_visit = subject_visit, panel = panel)
        self.assertEqual(Aliquot.objects.all().count(), 0)
        subjects_requisition.is_receive = True
        subjects_requisition.is_receive_datetime = datetime.now()
        subjects_requisition.save()
        lab_profile = site_lab_profiles.get(subjects_requisition._meta.object_name)
        lab_profile().receive(subjects_requisition)
        self.assertEqual(Aliquot.objects.all().count(), 1)
        aliquot = Aliquot.objects.all()[0]
        processing = ProcessingFactory(profile=AliquotProfile.objects.all()[0], aliquot=aliquot)
        for al in Aliquot.objects.all():
            instances.append(al)
        instances.append(processing)
        self.assertEqual(PackingListItem.objects.all().count(), 0)
        packing_list = PackingListFactory(list_items=aliquot.aliquot_identifier)
        self.assertEqual(PackingListItem.objects.all().count(), 1)
        instances.append(packing_list)
        instances.append(PackingListItem.objects.all()[0])

        print 'INSTANCE: ' + str(instances)
        for obj in instances:
            print 'test natural key on {0}'.format(obj._meta.object_name)
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        # pp = pprint.PrettyPrinter(indent=4)
        for obj in instances:
            print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj)
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
