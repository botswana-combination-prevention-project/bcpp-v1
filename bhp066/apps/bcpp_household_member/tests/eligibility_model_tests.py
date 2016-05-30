from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_map.classes import Mapper, site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.models import HouseholdStructure, Household
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.models import EnrollmentChecklist
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey


class TestPlotMapper(Mapper):
    map_area = 'test_community3'
    map_code = '091'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class EligibilityModelTests(TestCase):

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

    def test_new_member1(self):
        """Assert is eligible member."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',  # on day of survey
            study_resident='Yes')
        self.assertTrue(household_member.eligible_member)
        self.assertFalse(household_member.eligible_subject)
        self.assertFalse(household_member.eligible_htc)
        self.assertFalse(household_member.is_consented)
        self.assertFalse(household_member.is_htc_only)

    def test_new_member2(self):
        """Assert non study resident is not an eligible member."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',  # on day of survey
            study_resident='No')
        self.assertFalse(household_member.eligible_member)
        self.assertFalse(household_member.eligible_subject)
        self.assertFalse(household_member.eligible_htc)
        self.assertFalse(household_member.is_consented)
        self.assertFalse(household_member.is_htc_only)

    def test_new_member3(self):
        """Assert over 64 is not an eligible member."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=65,
            present_today='No',  # on day of survey
            study_resident='Yes')
        self.assertFalse(household_member.eligible_member)
        self.assertFalse(household_member.eligible_subject)
        self.assertFalse(household_member.eligible_htc)
        self.assertFalse(household_member.is_consented)
        self.assertFalse(household_member.is_htc_only)

    def test_new_member4(self):
        """Assert 15 is not an eligible member."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=15,
            present_today='No',  # on day of survey
            study_resident='Yes')
        self.assertFalse(household_member.eligible_member)
        self.assertFalse(household_member.eligible_subject)
        self.assertFalse(household_member.eligible_htc)
        self.assertFalse(household_member.is_consented)
        self.assertFalse(household_member.is_htc_only)

    def test_eligible_subject1(self):
        """Assert 'eligible' and 'is' flags  if passes enrollment checklist for BHS."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',  # on day of survey
            study_resident='Yes')
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=50),
            initials=household_member.initials)
        self.assertTrue(household_member.eligible_member)
        self.assertTrue(household_member.eligible_subject)
        self.assertFalse(household_member.eligible_htc)
        self.assertFalse(household_member.is_consented)
        self.assertFalse(household_member.is_htc_only)

    def test_eligible_subject2(self):
        """Assert 'eligible' and 'is' flags  if fails enrollment checklist for BHS but household not enrolled.

        Fails eligibility but is eligible for HTC by age."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',  # on day of survey
            study_resident='No')
        # should not be able get to this via the interface
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=50),
            initials=household_member.initials,
            part_time_resident='No')
        self.assertFalse(household_member.eligible_member)
        self.assertFalse(household_member.eligible_subject)
        self.assertFalse(household_member.eligible_htc)
        self.assertFalse(household_member.is_consented)
        self.assertFalse(household_member.is_htc_only)

    def test_eligible_subject3(self):
        """Assert 'eligible' and 'is' flags  if fails enrollment checklist for BHS and household is enrolled.

        Fails eligibility but is eligible for HTC by age."""
        # eligible member
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=25,
            study_resident='Yes',
            initials='EE')
        # who is an eligible subject
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            initials=household_member.initials,
            part_time_resident='Yes')
        # who is consented
        SubjectConsentFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            first_name='ERIKFIRST',
            last_name='ERIKLAST',
            initials=household_member.initials,)
        # the household is now enrolled
        self.assertTrue(household_member.household_structure.household.enrolled)
        # an ineligible member
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=65,
            study_resident='No')
        # who fails eligibility ...should not be able get to this via the interface
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=65),
            initials=household_member.initials,
            part_time_resident='No')
        # should only be eligible_htc
        self.assertFalse(household_member.eligible_member)
        self.assertFalse(household_member.eligible_subject)
        self.assertTrue(household_member.eligible_htc)
        self.assertFalse(household_member.is_consented)
        self.assertFalse(household_member.is_htc_only)

    def test_eligible_subject4(self):
        """Assert 'eligible' and 'is' flags  if passes enrollment checklist for BHS and household is enrolled."""
        # eligible member
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=25,
            study_resident='Yes',
            initials='EE')
        # who is an eligible subject
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            initials=household_member.initials,
            part_time_resident='Yes')
        # who is consented
        SubjectConsentFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            first_name='ERIKFIRST',
            last_name='ERIKLAST',
            initials=household_member.initials,)
        self.assertTrue(household_member.eligible_member)
        self.assertTrue(household_member.eligible_subject)
        self.assertFalse(household_member.eligible_htc)
        self.assertTrue(household_member.is_consented)
        self.assertFalse(household_member.is_htc_only)

    def test_enrollment_checklist_saved_on_success(self):
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',  # on day of survey
            study_resident='Yes')
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=50),
            initials=household_member.initials,
            part_time_resident='Yes')
        self.assertEqual(EnrollmentChecklist.objects.filter(household_member=household_member).count(), 1)

    def test_enrollment_checklist_deleted_on_fail(self):
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',  # on day of survey
            study_resident='No')
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=50),
            initials=household_member.initials,
            part_time_resident='No')
        self.assertEqual(EnrollmentChecklist.objects.filter(household_member=household_member).count(), 0)

    def test_updates_household_structure_counts(self):
        """Assert household_member updates household structure member_count and enrolled_member_count."""
        self.assertEquals(self.household_structure.member_count, 0)
        self.assertEquals(self.household_structure.enrolled_member_count, 0)
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=25,
            study_resident='Yes',
            initials='EE')
        # who is an eligible subject
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            initials=household_member.initials,
            part_time_resident='Yes')
        self.assertEquals(HouseholdStructure.objects.get(pk=self.household_structure.pk).member_count, 1)
        self.assertEquals(HouseholdStructure.objects.get(pk=self.household_structure.pk).enrolled_member_count, 0)
        # who is consented
        SubjectConsentFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            first_name='ERIKFIRST',
            last_name='ERIKLAST',
            initials=household_member.initials,)
        self.assertTrue(household_member.is_consented)
        self.assertEquals(HouseholdStructure.objects.get(pk=self.household_structure.pk).member_count, 1)
        self.assertEquals(HouseholdStructure.objects.get(pk=self.household_structure.pk).enrolled_member_count, 1)
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=35,
            study_resident='Yes',
            initials='DD')
        # who is an eligible subject
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=35),
            initials=household_member.initials,
            part_time_resident='Yes')
        self.assertEquals(HouseholdStructure.objects.get(pk=self.household_structure.pk).member_count, 2)
        # who is consented
        SubjectConsentFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=35),
            first_name='DRIKFIRST',
            last_name='DRIKLAST',
            initials=household_member.initials,)
        self.assertEquals(HouseholdStructure.objects.get(pk=self.household_structure.pk).member_count, 2)
        self.assertEquals(HouseholdStructure.objects.get(pk=self.household_structure.pk).enrolled_member_count, 2)

    def test_age_match(self):
        """Assert raises ValidationError if household_member age <> enrollment age."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=25,
            study_resident='Yes',
            initials='EE')
        self.assertRaisesRegexp(ValidationError, 'Age does not match', EnrollmentChecklistFactory,
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=35),
            initials=household_member.initials,
            part_time_resident='Yes')

    def test_age_match2(self):
        """Assert raises ValidationError if household_member age <> enrollment age."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=35,
            study_resident='Yes',
            initials='EE')
        self.assertRaisesRegexp(ValidationError, 'Age does not match', EnrollmentChecklistFactory,
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            initials=household_member.initials,
            part_time_resident='Yes')

    def test_age_match3(self):
        """Assert raises ValidationError if household_member age <> enrollment age."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=75,
            study_resident='Yes',
            initials='EE')
        self.assertRaisesRegexp(ValidationError, 'Age does not match', EnrollmentChecklistFactory,
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            initials=household_member.initials,
            part_time_resident='Yes')

    def test_residency_match(self):
        """Assert raises ValidationError if household_member age <> enrollment age."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=25,
            study_resident='No',
            initials='EE')
        self.assertRaisesRegexp(ValidationError, 'Residency does not match', EnrollmentChecklistFactory,
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            initials=household_member.initials,
            part_time_resident='Yes')

    def test_initials_match(self):
        """Assert raises ValidationError if household_member age <> enrollment age."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=25,
            study_resident='Yes',
            initials='EE')
        self.assertRaisesRegexp(ValidationError, 'Initials do not match', EnrollmentChecklistFactory,
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            initials="XX",
            part_time_resident='Yes')

    def test_gender_match(self):
        """Assert raises ValidationError if household_member age <> enrollment age."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=25,
            study_resident='Yes',
            initials='EE')
        self.assertRaisesRegexp(ValidationError, 'Gender does not match', EnrollmentChecklistFactory,
            household_member=household_member,
            gender='F',
            dob=date.today() - relativedelta(years=25),
            initials="EE",
            part_time_resident='Yes')
