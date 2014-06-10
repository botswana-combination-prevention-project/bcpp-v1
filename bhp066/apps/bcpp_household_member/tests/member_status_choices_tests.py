from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import Mapper, site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_household.tests.factories import PlotFactory
from apps.bcpp_household_member.models import HouseholdMember, EnrollmentChecklist
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory, SubjectRefusalFactory
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.tests.factories import SubjectConsentFactory
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_survey.models import Survey
from apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory

from ..constants import  ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC, HTC_ELIGIBLE, NOT_ELIGIBLE, REFUSED, UNDECIDED 


class TestPlotMapper(Mapper):
    map_area = 'test_community6'
    map_code = '094'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()
site_mappers.register(TestPlotMapper)


class MemberStatusChoicesTests(TestCase):
    def __init__(self, *args, **kwargs):
        self.household_member = None
        self.subject_consent = None
        self.enrollment_checklist = None
        self.registered_subject = None
        self.study_site = None
        super(MemberStatusChoicesTests, self).__init__(*args, **kwargs)

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
        self.representative_eligibility = RepresentativeEligibilityFactory(household_structure=self.household_structure)

    def enroll_household(self):
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=18, study_resident='Yes', household_structure=self.household_structure)
        pk = household_member.pk
        self.assertTrue(isinstance(EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=18),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes'), EnrollmentChecklist))
        household_member = HouseholdMember.objects.get(pk=pk)
        SubjectConsentFactory(
            household_member=household_member,
            first_name="ERIK",
            last_name='WERIK',
            gender='M',
            dob=date.today() - relativedelta(years=18),
            initials=household_member.initials)
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, BHS)
        self.household_structure = household_member.household_structure
        self.assertTrue(household_member.household_structure.enrolled)
        return household_member

    def test_new_eligible_member(self):
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=64, study_resident='Yes', household_structure=self.household_structure)
        options = [ABSENT, BHS_SCREEN, REFUSED, UNDECIDED]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
#         print x
#         print member_status_choices
        self.assertEqual(x, member_status_choices)

    def test_not_eligible_member(self):
        """Assert for not eligible for BHS and HTC (household not enrolled)."""
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=64, study_resident='No', household_structure=self.household_structure)
        options = [NOT_ELIGIBLE]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        self.assertEqual(household_member.member_status_choices, member_status_choices)

    def test_eligible_htc_only(self):
        """Assert for not eligible for BHS but eligible for HTC (household enrolled). No need to ever screen for BHS as not eligible member(by age or residency)."""
        self.enroll_household()
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=64, study_resident='No', household_structure=self.household_structure)
        options = [HTC_ELIGIBLE, BHS_SCREEN]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        self.assertEqual(household_member.member_status_choices, member_status_choices)

    def test_eligible_htc_with_bhs_screen_option(self):
        """Assert for not eligible for BHS but eligible for HTC (household enrolled), but with option to still screen for BHS in case eligibility information changes"""
        self.enroll_household()
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=64, study_resident='Yes', household_structure=self.household_structure)
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=64),
            guardian='No',
            has_identity='No',
            initials=household_member.initials,
            part_time_resident='Yes')
        options = [BHS_SCREEN, HTC_ELIGIBLE]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status_choices, member_status_choices)

    def test_eligible_member_bhs_and_htc(self):
        """Assert for not eligible for BHS but eligible for HTC (household enrolled)."""
        self.enroll_household()
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=78, study_resident='Yes', household_structure=self.household_structure)
        self.assertEqual(household_member.member_status, HTC_ELIGIBLE)
        options = [HTC_ELIGIBLE, BHS_SCREEN]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
#         print x
#         print member_status_choices
        self.assertEqual(x, member_status_choices)

    def test_eligible_bhs_and_htc_and_refused_bhs(self):
        """Assert for eligible for BHS, household is enrolled, and eligible for HTC since has refused BHS."""
        self.enroll_household()
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=64, study_resident='Yes', household_structure=self.household_structure)
        household_member.member_status = REFUSED
        household_member.save()
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, REFUSED)
        SubjectRefusalFactory(household_member=household_member)
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, HTC_ELIGIBLE)
        self.assertTrue(household_member.refused)
        self.assertTrue(household_member.eligible_htc)
        options = [BHS_SCREEN, HTC_ELIGIBLE]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
        self.assertEqual(x, member_status_choices)

    def test_refused_bhs_and_consent_later(self):
        """Assert for refused BHS, household not enrolled and BHS_SCREEN still available as option."""
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=64, study_resident='Yes', household_structure=self.household_structure)
        household_member.member_status = REFUSED
        household_member.save()
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, REFUSED)
        SubjectRefusalFactory(household_member=household_member)
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, REFUSED)
        self.assertTrue(household_member.refused)
        options = [BHS_SCREEN]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        print options
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
        print x
        self.assertEqual(x, member_status_choices)

    def test_eligible_bhs(self):
        """Assert for eligible for BHS, household enrolled."""
        self.enroll_household()
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=64, study_resident='Yes', household_structure=self.household_structure)
        household_member.member_status = BHS_SCREEN
        household_member.save()
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=64),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes')
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        options = [BHS, BHS_ELIGIBLE, REFUSED]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
#         print x
#         print member_status_choices
        self.assertEqual(x, member_status_choices)

#     def test_invalid_conditions(self):
#         """Assert for failure to pick up valid tuple condition, an in-eligible_member that is also a refusal"""
#         self.enroll_household()
#         household_member = HouseholdMemberFactory(first_name='ERIK', initials='EXW', age_in_years=64, study_resident='No', household_structure=self.household_structure)
#         pk = household_member.pk
#         household_member = HouseholdMember.objects.get(pk=pk)
#         household_member.member_status = REFUSED
#         household_member.save()
#         pk = household_member.pk
#         household_member = HouseholdMember.objects.get(pk=pk)
#         self.assertRaises(TypeError, lambda: SubjectRefusalFactory(household_member=household_member))
#         print household_member.member_status

    def test_consented(self):
        """Assert only returns BHS if member is consented."""
        household_member = self.enroll_household()
        self.assertTrue(household_member.is_consented)
        options = [BHS]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
#         print member_status_choices
#         print household_member.member_status_choices
        self.assertEqual(household_member.member_status_choices, member_status_choices)
