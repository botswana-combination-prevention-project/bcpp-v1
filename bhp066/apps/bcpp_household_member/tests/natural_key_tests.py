from datetime import datetime, timedelta, date
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.models import signals
from django.core import serializers
from django.db.models import get_app, get_models

from edc.core.crypto_fields.classes import FieldCryptor
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.device.sync.classes import SerializeToTransaction
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_survey.models import Survey
from apps.bcpp_household.tests.factories import HouseholdStructureFactory, RepresentativeEligibilityFactory
from apps.bcpp_household.models import post_save_on_household, create_household_on_post_save, household_structure_on_post_save
from .factories import (HouseholdMemberFactory, EnrollmentChecklistFactory, HouseholdInfoFactory, SubjectMovedFactory, SubjectAbsenteeEntryFactory,
                        SubjectUndecidedEntryFactory, SubjectAbsenteeFactory, SubjectUndecidedFactory, EnrollmentLossFactory,
                        HeadHouseholdEligibilityFactory, SubjectHtcFactory)
from apps.bcpp_household_member.models import EnrollmentLoss, SubjectRefusalHistory, SubjectRefusal


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
        app = get_app('bcpp_household_member')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name and  model._meta.object_name != 'EnrollmentChecklist':
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_household_member')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:# and  model._meta.object_name != 'EnrollmentChecklist':
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        survey = Survey.objects.all()[0]
        from apps.bcpp_household.models import HouseholdStructure
        signals.post_save.disconnect(post_save_on_household, weak=False, dispatch_uid="post_save_on_household")
        signals.post_save.disconnect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        signals.post_save.disconnect(post_save_on_household, weak=False, dispatch_uid="post_save_on_household")
        household_structure = HouseholdStructureFactory(survey=survey)
        representative_eligibility = RepresentativeEligibilityFactory(household_structure=household_structure)
        signals.post_save.connect(post_save_on_household, weak=False, dispatch_uid="post_save_on_household")
        signals.post_save.connect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        signals.post_save.connect(create_household_on_post_save, weak=False, dispatch_uid="create_household_on_post_save")
        household_member = HouseholdMemberFactory(age_in_years=16, household_structure=household_structure, survey=survey)
        #loss = EnrollmentLossFactory(household_member = household_member)
        print 'get registered subject'
        registered_subject = RegisteredSubject.objects.get(subject_identifier=household_member.registered_subject.subject_identifier)
        from .factories import SubjectRefusalFactory
        household_member.member_status = 'REFUSED'
        subject_refusal = SubjectRefusalFactory(household_member=household_member)
        SubjectRefusal.objects.get(household_member=household_member).delete()
        subject_refusal_history = SubjectRefusalHistory.objects.get(household_member=household_member)
        print 'Enrollment Loss count='+str(EnrollmentLoss.objects.all().count())
        household_member.member_status = 'BHS_SCREEN'
        enrollment_checklist = EnrollmentChecklistFactory(household_member=household_member, initials=household_member.initials, has_identity='No')
        print 'Enrollment Loss count='+str(EnrollmentLoss.objects.all().count())
        #loss = EnrollmentLoss.objects.get(household_member=household_member)
        household_member.member_status = 'HTC_ELIGIBLE'
        subject_htc = SubjectHtcFactory(household_member=household_member)
        self.assertRaises(ValidationError, lambda: HouseholdInfoFactory(household_structure=household_structure, household_member=household_member))
        household_member.age_in_years = 19
        household_head_eligibility = HeadHouseholdEligibilityFactory(household_member=household_member)
        household_info = HouseholdInfoFactory(household_structure=household_structure, household_member=household_member)
        subject_absentee = SubjectAbsenteeFactory(household_member=household_member, registered_subject=registered_subject)
        subject_undecided = SubjectUndecidedFactory(household_member=household_member, registered_subject=registered_subject)
        subject_moved = SubjectMovedFactory(household_member=household_member, registered_subject=registered_subject)
        subject_absentee_entry = SubjectAbsenteeEntryFactory(subject_absentee=subject_absentee, report_datetime=date.today())
        subject_undecided_entry = SubjectUndecidedEntryFactory(subject_undecided=subject_undecided, report_datetime=date.today())
        subject_absentee_entry1 = SubjectAbsenteeEntryFactory(subject_absentee=subject_absentee, report_datetime=date.today()+timedelta(days=int(2)))
        subject_undecided_entry1 = SubjectUndecidedEntryFactory(subject_undecided=subject_undecided, report_datetime=date.today()+timedelta(days=int(2)))

        instances = []
        instances.append(household_member)
        instances.append(registered_subject)
        instances.append(enrollment_checklist)
        instances.append(household_structure)
        instances.append(household_info)
        #instances.append(subject_refusal)
        instances.append(subject_htc)
        instances.append(subject_refusal_history)
        #instances.append(loss)
        instances.append(household_head_eligibility)
        instances.append(subject_moved)
        instances.append(subject_absentee_entry)
        instances.append(subject_undecided_entry)
        instances.append(subject_absentee_entry1)
        instances.append(subject_undecided_entry1)

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
            # pp.pprint(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
