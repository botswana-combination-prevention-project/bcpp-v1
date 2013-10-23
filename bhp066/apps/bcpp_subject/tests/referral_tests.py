from datetime import datetime, date
from django.test import TestCase

from edc.map.classes import Mapper, site_mappers
from edc.subject.registration.models import RegisteredSubject
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_survey.tests.factories import SurveyFactory
from apps.bcpp_household.tests.factories import PlotFactory, HouseholdFactory, HouseholdStructureFactory
from apps.bcpp_household.models import Plot, Household, HouseholdStructure
from apps.bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory, SubjectReferralFactory

from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory


class TestPlotMapper(Mapper):
    map_area = 'test_community1'
    map_code = '099'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747132
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class ReferralTests(TestCase):

    app_label = 'bcpp_subject'

    def setUp(self):
        self.survey = SurveyFactory()
        site_lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(content_type__model='SubjectConsent'.lower())
        ConsentCatalogueFactory(
            name=self.app_label,
            consent_type='study',
            content_type_map=content_type_map,
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='survey', grouping_key='SURVEY')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='subjectvisit')
        visit_definition = VisitDefinitionFactory(code='T0', title='T0', grouping='subject', visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        plot = PlotFactory(community='test_community1', household_count=1, status='occupied')
        self.assertEqual(Plot.objects.all().count(), 1)
        self.assertEqual(Household.objects.all().count(), 1)
        self.assertEqual(HouseholdStructure.objects.all().count(), 1)
        household_structure = HouseholdStructure.objects.get(household__plot=plot)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        self.household_member_female = HouseholdMemberFactory(household_structure=household_structure, gender='F')
        self.household_member_male = HouseholdMemberFactory(household_structure=household_structure, gender='M')
        self.household_member_female.eligible_member = True
        self.household_member_male.eligible_member = True
        self.household_member_female.eligible_subject = True
        self.household_member_male.eligible_subject = True
        self.household_member_female.save()
        self.household_member_male.save()
        subject_consent_female = SubjectConsentFactory(household_member=self.household_member_female)
        subject_consent_male = SubjectConsentFactory(household_member=self.household_member_male)
        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=subject_consent_male.subject_identifier)
        appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female)
        self.subject_visit_female = SubjectVisitFactory(appointment=appointment_female, household_member=self.household_member_female)
        appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male)
        self.subject_visit_male = SubjectVisitFactory(appointment=appointment_male, household_member=self.household_member_male)

    def tests_referred_hiv(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='IND')
        self.assertIn('HIV', subject_referral.referral_code_list)

    def tests_referred_hiv_urgent(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='IND')
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_neg_male(self):
        """if NEG and male, refer for SMC"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='NEG',
            gender='M')
        self.assertIn('SMC', subject_referral.referral_code_list)

    def tests_not_referred_neg_female(self):
        """if NEG and female, no referral"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            hiv_result='NEG',
            gender='F')
        self.assertEquals('', subject_referral.referral_code_list)

    def tests_referred_cd4(self):
        """if POS but no other data, refer for CD4"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=None)
        self.assertIn('CD4', subject_referral.referral_code_list)

    def tests_referred_cd4_urgent(self):
        """if POS but no other data, refer for CD4"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=None)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_ccc1(self):
        """if POS, high CD4 and art unknown, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=350)
        self.assertIn('CCC', subject_referral.referral_code_list)

    def tests_referred_ccc2(self):
        """if POS, low CD4 and art unknown, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=349)
        self.assertIn('CCC-LOW', subject_referral.referral_code_list)

    def tests_referred_ccc2_urgent(self):
        """if POS, low CD4 and art unknown, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=None,
            cd4_result=349)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_ccc3(self):
        """if pos, high CD4 and not on art, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=False,
            cd4_result=351)
        self.assertIn('CCC-HIGH', subject_referral.referral_code_list)

    def tests_referred_masa1(self):
        """if pos, low CD4 and not on art, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=False,
            cd4_result=349)
        self.assertIn('CCC-LOW', subject_referral.referral_code_list)

    def tests_referred_masa1_urgent(self):
        """if pos, low CD4 and not on art, should be urgent"""
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=False,
            cd4_result=349)
        self.assertTrue(subject_referral.urgent_referral)

    def tests_referred_masa2(self):
        """if pos, high CD4 and on art, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=True,
            cd4_result=351)
        self.assertIn('MASA-HIGH', subject_referral.referral_code_list)

    def tests_referred_masa3(self):
        """if pos, low CD4 and on art, """
        report_datetime = datetime.today()
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime,
            hiv_result='POS',
            hiv_result_datetime=datetime.today(),
            on_art=True,
            cd4_result=350)
        self.assertIn('MASA-LOW', subject_referral.referral_code_list)


""" If HIV positive on ART
    - record date of next scheduled refill or clinic visit (should be recorded on OPD card)
    - record clinic to be attended

If HIV positive not on ART
- record date of scheduled clinic visit (should be within 1wk if possible and on the next available ART clinic day)
- record date of clinic to be attended

If HIV negative
- record date for scheduled counseling regarding SMC
- record location of referral for SMC counseling"""
