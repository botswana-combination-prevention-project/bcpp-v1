from datetime import date, datetime, timedelta
from dateutils import relativedelta
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import Mapper, site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.models import Loss, HouseholdMember, SubjectRefusal, SubjectAbsentee, EnrolmentChecklist
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrolmentChecklistFactory, SubjectRefusalFactory, SubjectUndecidedFactory
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.tests.factories import SubjectConsentFactory
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_survey.models import Survey

from ..exceptions import MemberStatusError
from ..constants import  ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC, HTC_ELIGIBLE, NOT_ELIGIBLE, NOT_REPORTED, REFUSED, UNDECIDED


class TestPlotMapper(Mapper):
    map_area = 'test_community5'
    map_code = '093'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()
site_mappers.register(TestPlotMapper)


class MemberStatusTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.household_member = None
        self.subject_consent = None
        self.enrollment_checklist = None
        self.registered_subject = None
        self.study_site = None
        super(MemberStatusTests, self).__init__(*args, **kwargs)

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        plot = PlotFactory(community='test_community3', household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        self.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)

    def test_household_member1(self):
        """Assert not reported based on age and residency"""
        HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=64, study_resident='Yes', household_structure=self.household_structure)
        household_member = HouseholdMember.objects.get(household_structure=self.household_structure)
        self.assertTrue(household_member.member_status == NOT_REPORTED)

    def test_household_member1a(self):
        """Assert not reported based on age and residency, household not enrolled"""
        HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=64, study_resident='No', household_structure=self.household_structure)
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)

    def test_household_member2(self):
        """Assert not reported based on age and residency, household not enrolled"""
        HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=75, study_resident='Yes', household_structure=self.household_structure)
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)

    def test_household_member2a(self):
        """Assert not reported based on age and residency, household not enrolled"""
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=75, study_resident='No', household_structure=self.household_structure)
        self.assertTrue(HouseholdMember.objects.get(household_structure=self.household_structure).member_status == NOT_ELIGIBLE)

    def test_household_member3(self):
        """Assert not eligible based on age and residency"""
        HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=15, study_resident='Yes', household_structure=self.household_structure)
        self.assertTrue(HouseholdMember.objects.get(household_structure=self.household_structure).member_status == NOT_ELIGIBLE)

    def test_household_member3a(self):
        """Assert not eligible based on age and residency"""
        HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=15, study_resident='No', household_structure=self.household_structure)
        self.assertTrue(HouseholdMember.objects.get(household_structure=self.household_structure).member_status == NOT_ELIGIBLE)

    def test_household_member4(self):
        """Assert not reported based on age and residency"""
        HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=16, study_resident='Yes', household_structure=self.household_structure)
        self.assertTrue(HouseholdMember.objects.get(household_structure=self.household_structure).member_status == NOT_REPORTED)

    def test_household_member5(self):
        """Assert not reported based on age and residency"""
        HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=16, study_resident='No', household_structure=self.household_structure)
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)

    def enroll_household(self):
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=18, study_resident='Yes', household_structure=self.household_structure)
        household_member.member_status = 'BHS_SCREEN'
        household_member.created = datetime.today() - timedelta(days=1)
        household_member.save()
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertTrue(isinstance(EnrolmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=18),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes'), EnrolmentChecklist))
        SubjectConsentFactory(
            household_member=household_member,
            first_name="ERIK",
            last_name='WERIK',
            gender='M',
            dob=date.today() - relativedelta(years=18),
            initials=household_member.initials)
        return HouseholdMember.objects.get(pk=pk)

    def test_enrolled_household(self):
        """Assert household is enrolled when subject consents"""
        household_member = self.enroll_household()
        self.assertTrue(household_member.household_structure.enrolled)

    def test_enrolled_household1(self):
        """Assert is HTC eligible if not BHS eligible based on residency and household is enrolled"""
        household_member = self.enroll_household()
        household_structure = HouseholdMember.objects.get(household_structure=household_member.household_structure).household_structure
        HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=64, study_resident='No', household_structure=household_structure)
        self.assertEqual(HouseholdMember.objects.get(initials='EXW', household_structure=household_structure).member_status, HTC_ELIGIBLE)

    def test_enrolled_household2(self):
        """Assert is HTC eligible if not BHS eligible based on age (adult) and household is enrolled"""
        household_member = self.enroll_household()
        household_structure = HouseholdMember.objects.get(household_structure=household_member.household_structure).household_structure
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=75, study_resident='Yes', household_structure=household_structure)
        self.assertEqual(HouseholdMember.objects.get(initials='EXW', household_structure=household_structure).member_status, HTC_ELIGIBLE)

    def test_enrolled_household3(self):
        """Assert is HTC eligible if not BHS eligible based on age (adult) and residency and household is enrolled"""
        household_member = self.enroll_household()
        household_structure = HouseholdMember.objects.get(household_structure=household_member.household_structure).household_structure
        HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=75, study_resident='No', household_structure=household_structure)
        self.assertTrue(HouseholdMember.objects.get(initials='EXW', household_structure=household_structure).member_status == HTC_ELIGIBLE)

    def test_enrolled_household4(self):
        """Assert is NOT eligible for BHS and HTC based on age (minor) and household is enrolled"""
        household_member = self.enroll_household()
        household_structure = HouseholdMember.objects.get(household_structure=household_member.household_structure).household_structure
        HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=15, study_resident='Yes', household_structure=household_structure)
        self.assertTrue(HouseholdMember.objects.get(initials='EXW', household_structure=household_structure).member_status == NOT_ELIGIBLE)

    def test_enrolled_household5(self):
        """Assert is NOT eligible for BHS and HTC based on age (minor) and residency and household is enrolled"""
        household_member = self.enroll_household()
        household_structure = HouseholdMember.objects.get(household_structure=household_member.household_structure).household_structure
        HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=15, study_resident='No', household_structure=household_structure)
        self.assertTrue(HouseholdMember.objects.get(initials='EXW', household_structure=household_structure).member_status == NOT_ELIGIBLE)

    def test_household_member6(self):
        """Assert auto sets to absent if new instance and not present today."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',
            study_resident='Yes')
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, ABSENT)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=household_member).count(), 1)

    def test_change_household_member1(self):
        """Assert not absent if not new instance."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        household_member.present_today = 'No'
        household_member.save()
        self.assertEqual(SubjectAbsentee.objects.filter(household_member=household_member).count(), 0)
        self.assertTrue(HouseholdMember.objects.get(household_structure=self.household_structure).member_status == NOT_REPORTED)

    def test_change_household_member2(self):
        """Assert cannot enter Enrolment Checklist if absent"""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',
            study_resident='Yes')
        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        self.assertEquals(household_member.member_status, ABSENT)
        self.assertRaisesRegexp(MemberStatusError, BHS_SCREEN, EnrolmentChecklistFactory,
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=50),
            initials=household_member.initials,
            part_time_resident='Yes')

    def test_change_household_member3(self):
        """Assert can enter Enrolment Checklist if not present "today" but member was created yesterday."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',
            study_resident='Yes')
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        household_member.member_status = 'BHS_SCREEN'
        household_member.created = datetime.today() - timedelta(days=1)
        household_member.save()
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertTrue(isinstance(EnrolmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=50),
            initials=household_member.initials,
            part_time_resident='Yes'), EnrolmentChecklist))
        self.assertEquals(household_member.member_status, BHS_ELIGIBLE)

    def test_change_household_member4(self):
        """Assert can set to REFUSED but household_member.refused is False."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        household_member.member_status = REFUSED
        household_member.save()
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, REFUSED)
        self.assertFalse(household_member.refused)

    def test_change_household_member5(self):
        """Assert sets to REFUSED as refusal form is added, refused is True."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        household_member.member_status = REFUSED
        household_member.save()
        household_member = HouseholdMember.objects.get(pk=pk)
        SubjectRefusalFactory(household_member=household_member)
        self.assertEqual(household_member.member_status, REFUSED)
        self.assertTrue(household_member.refused)
