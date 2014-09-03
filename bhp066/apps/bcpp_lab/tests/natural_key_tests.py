from datetime import datetime, date
from django.core import serializers
from django.db.models import get_app, get_models
from django.test import TestCase

from edc.core.bhp_variables.models import StudySite
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.core.crypto_fields.classes import FieldCryptor
from edc.device.sync.classes import SerializeToTransaction
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.appointment.models import Appointment
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_subject.tests.factories import (SubjectConsentFactory, SubjectVisitFactory)
from apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from apps.bcpp_household.models import Household, HouseholdStructure, Survey
from apps.bcpp_household_member.tests.factories import EnrollmentChecklistFactory, HouseholdMemberFactory
from apps.bcpp_lab.tests.factories import (SubjectRequisitionFactory, ProcessingFactory, PackingListFactory)
from apps.bcpp_lab.models import Aliquot, Panel, AliquotProfile, PackingListItem, AliquotType, Receive
from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile


class NaturalKeyTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_lab')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_lab')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        instances = []
        plot = PlotFactory(community='test_community6', household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=Survey.objects.all()[0])
        representative_eligibility = RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(household_structure=household_structure)
        enrollment_checklist = EnrollmentChecklistFactory(household_member=household_member, initials=household_member.initials, has_identity='Yes', dob=date(1989, 01, 01))
        self.assertTrue(enrollment_checklist.is_eligible)
        instances.append(enrollment_checklist)
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)
        registered_subject = RegisteredSubject.objects.all()[0]
        site = StudySite.objects.all()[0]
        subject_consent = SubjectConsentFactory(study_site=site, household_member=household_member, registered_subject=household_member.registered_subject,
                                                dob=enrollment_checklist.dob, initials=enrollment_checklist.initials)
        instances.append(subject_consent)
        self.assertEqual(Appointment.objects.all().count(), 1)
        appointment = Appointment.objects.get(registered_subject = registered_subject)
        subject_visit = SubjectVisitFactory(household_member=household_member, appointment = appointment)
        instances.append(subject_visit)
        aliquot_type = AliquotType.objects.all()[0]
        panel = Panel.objects.all()[0]
        subjects_requisition = SubjectRequisitionFactory(subject_visit=subject_visit, panel=panel, site=site, aliquot_type=aliquot_type,)
        self.assertEqual(Aliquot.objects.all().count(), 0)
        subjects_requisition.is_receive = True
        subjects_requisition.is_receive_datetime = datetime.now()
        subjects_requisition.save()
        lab_profile = site_lab_profiles.get(subjects_requisition._meta.object_name)
        lab_profile().receive(subjects_requisition)
        receive = Receive.objects.all()[0]
        self.assertEqual(Aliquot.objects.all().count(), 1)
        aliquot = Aliquot.objects.all()[0]
        processing = ProcessingFactory(profile=AliquotProfile.objects.all()[0], aliquot=aliquot)
        for al in Aliquot.objects.all():
            instances.append(al)
        instances.append(processing)
        instances.append(receive)
        self.assertEqual(PackingListItem.objects.all().count(), 0)
        packing_list = PackingListFactory(list_items=aliquot.aliquot_identifier)
        instances.append(packing_list)
        packing_list.list_items = al.aliquot_identifier
        print packing_list.list_items
        packing_list.save()
        #self.assertEquals(PackingListItem.objects.all().count(), 1)
        #instances.append(PackingListItem.objects.all()[0])

        print 'INSTANCE: ' + str(instances)
        for obj in instances:
            print 'test natural key on {0}'.format(obj._meta.object_name)
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        # pp = pprint.PrettyPrinter(indent=4)
        for obj in instances:
            print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj, False, True, 'default')
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
