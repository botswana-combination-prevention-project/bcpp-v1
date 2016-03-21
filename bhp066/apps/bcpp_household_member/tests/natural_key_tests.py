from datetime import datetime, timedelta, date
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.models import signals
from django.core import serializers
from django.db.models import get_app, get_models

from edc_base.encrypted_fields import FieldCryptor
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.device.sync.classes import SerializeToTransaction
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.registration.models import RegisteredSubject

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory, PlotFactory
from bhp066.apps.bcpp_household.models import household_on_post_save, household_structure_on_post_save, Household
from .factories import (HouseholdMemberFactory, EnrollmentChecklistFactory, HouseholdInfoFactory, SubjectMovedFactory, SubjectAbsenteeEntryFactory,
                        SubjectUndecidedEntryFactory, SubjectAbsenteeFactory, SubjectUndecidedFactory, EnrollmentLossFactory,
                        HeadHouseholdEligibilityFactory, SubjectHtcFactory)
from bhp066.apps.bcpp_household_member.models import EnrollmentLoss, SubjectRefusalHistory, SubjectRefusal, EnrollmentChecklist


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
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_household_member')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:# and  model._meta.object_name != 'EnrollmentChecklist':
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        survey = Survey.objects.all()[0]
        from bhp066.apps.bcpp_household.models import HouseholdStructure
        plot = PlotFactory(community='test_community6', household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        signals.post_save.disconnect(household_on_post_save, weak=False, dispatch_uid="post_save_on_household")
        signals.post_save.disconnect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        household_structure = HouseholdStructure.objects.get(household=household, survey=survey)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        signals.post_save.connect(household_on_post_save, weak=False, dispatch_uid="post_save_on_household")
        signals.post_save.connect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        household_member = HouseholdMemberFactory(age_in_years=16, household_structure=household_structure, survey=survey)
        registered_subject = RegisteredSubject.objects.get(subject_identifier=household_member.registered_subject.subject_identifier)
        from .factories import SubjectRefusalFactory
        household_member.member_status = 'REFUSED'
        SubjectRefusalFactory(household_member=household_member)
        SubjectRefusal.objects.get(household_member=household_member).delete()
        subject_refusal_history = SubjectRefusalHistory.objects.get(household_member=household_member)
        self.assertEquals(EnrollmentLoss.objects.all().count(), 0)
        household_member.member_status = 'BHS_SCREEN'
        EnrollmentChecklistFactory(household_member=household_member, initials=household_member.initials, has_identity='No')
        self.assertEquals(EnrollmentLoss.objects.all().count(), 1)
        household_member.member_status = 'HTC_ELIGIBLE'
        subject_htc = SubjectHtcFactory(household_member=household_member)
        self.assertRaises(ValidationError, lambda: HouseholdInfoFactory(household_structure=household_structure, household_member=household_member))
        household_member.age_in_years = 19
        household_head_eligibility = HeadHouseholdEligibilityFactory(household_member=household_member)
        household_info = HouseholdInfoFactory(household_structure=household_structure, household_member=household_member)
        subject_absentee = SubjectAbsenteeFactory(household_member=household_member, registered_subject=registered_subject)
        self.assertEquals(EnrollmentChecklist.objects.all().count(), 0)
        subject_undecided = SubjectUndecidedFactory(household_member=household_member, registered_subject=registered_subject)
        subject_moved = SubjectMovedFactory(household_member=household_member, registered_subject=registered_subject)
        subject_absentee_entry = SubjectAbsenteeEntryFactory(subject_absentee=subject_absentee, report_datetime=date.today())
        subject_undecided_entry = SubjectUndecidedEntryFactory(subject_undecided=subject_undecided, report_datetime=date.today())
        subject_absentee_entry1 = SubjectAbsenteeEntryFactory(subject_absentee=subject_absentee, report_datetime=date.today()+timedelta(days=int(2)))
        subject_undecided_entry1 = SubjectUndecidedEntryFactory(subject_undecided=subject_undecided, report_datetime=date.today()+timedelta(days=int(2)))
        instances = []
        instances.append(household_member)
        instances.append(registered_subject)
        instances.append(household_structure)
        instances.append(household_info)
        instances.append(subject_htc)
        instances.append(subject_refusal_history)
        instances.append(household_head_eligibility)
        instances.append(subject_moved)
        instances.append(subject_absentee_entry)
        instances.append(subject_undecided_entry)
        instances.append(subject_absentee_entry1)
        instances.append(subject_undecided_entry1)

        for obj in instances:
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        for obj in instances:
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj, False, True, 'default')
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
