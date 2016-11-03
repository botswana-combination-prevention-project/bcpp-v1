from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.core.bhp_variables.models import StudySite

from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household_member.tests.factories import (
    HouseholdMemberFactory, EnrollmentChecklistFactory, SubjectRefusalFactory)
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory

from ..constants import ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC_ELIGIBLE, REFUSED, UNDECIDED, DECEASED


class TestMemberStatusChoices(TestCase):

    def setUp(self):

        from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration

        self.household_structure = None
        self.registered_subject = None
        self.representative_eligibility = None
        self.study_site = None
        self.intervention = None
        site_mappers.autodiscover()
        from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 2')  # see app_configuration
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        self.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        self.representative_eligibility = RepresentativeEligibilityFactory(
            household_structure=self.household_structure)
        self.study_site = StudySite.objects.get(
            site_code=site_mappers.get_mapper(site_mappers.current_community).map_code)
        self.intervention = site_mappers.get_mapper(site_mappers.current_community).intervention

    def enroll_household(self):
        household_member = HouseholdMemberFactory(
            first_name='ERIK',
            initials='EW',
            age_in_years=18,
            study_resident='Yes',
            household_structure=self.household_structure)
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=18),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes')
        from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
        subject_consent = SubjectConsentFactory(
            household_member=enrollment_checklist.household_member,
            first_name="ERIK",
            last_name='WERIK',
            gender='M',
            dob=date.today() - relativedelta(years=18),
            initials=household_member.initials,
            study_site=self.study_site,)
        self.assertEqual(subject_consent.household_member.member_status, BHS)
        self.household_structure = subject_consent.household_member.household_structure
        self.assertTrue(subject_consent.household_member.household_structure.enrolled)
        return household_member

    def test_new_eligible_member(self):
        household_member = HouseholdMemberFactory(
            first_name='ERIK',
            initials='EW',
            age_in_years=64,
            study_resident='Yes',
            household_structure=self.household_structure)
        options = [ABSENT, BHS_SCREEN, REFUSED, UNDECIDED, DECEASED]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
        self.assertEqual(x, member_status_choices)

    def test_eligible_htc_only(self):
        """Assert for not eligible for BHS but eligible for HTC (household enrolled).
        No need to ever screen for BHS as not eligible member(by age or residency)."""
        household_member = self.enroll_household()
        household_member = HouseholdMemberFactory(
            first_name='ERIK',
            initials='EXW',
            age_in_years=64,
            study_resident='No',
            household_structure=household_member.household_structure)
        self.assertEqual(household_member.member_status, HTC_ELIGIBLE)
        options = [BHS_SCREEN]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        self.assertEqual(household_member.member_status_choices, member_status_choices)

    def test_eligible_htc_with_bhs_screen_option(self):
        """Assert for not eligible for BHS but eligible for HTC (household enrolled),
        but with option to still screen for BHS in case eligibility information changes"""
        household_member = self.enroll_household()
        household_member = HouseholdMemberFactory(
            first_name='ERIK',
            initials='EXW',
            age_in_years=64,
            study_resident='Yes',
            household_structure=household_member.household_structure)
        self.assertTrue(household_member.household_structure.enrolled)
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=64),
            guardian='No',
            has_identity='No',
            initials=household_member.initials,
            part_time_resident='Yes')
        self.assertEqual(household_member.member_status, HTC_ELIGIBLE)
        options = [BHS_SCREEN, HTC_ELIGIBLE]
        options.append(enrollment_checklist.household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        self.assertEqual(enrollment_checklist.household_member.member_status_choices, member_status_choices)

    def test_eligible_member_bhs_and_htc(self):
        """Assert for not eligible for BHS but eligible for HTC (household enrolled)."""
        household_member = self.enroll_household()
        household_member = HouseholdMemberFactory(
            first_name='ERIK',
            initials='EXW',
            age_in_years=78,
            study_resident='Yes',
            household_structure=household_member.household_structure)
        self.assertEqual(household_member.member_status, HTC_ELIGIBLE)
        options = [HTC_ELIGIBLE, BHS_SCREEN]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
        self.assertEqual(x, member_status_choices)

    def test_eligible_bhs_and_htc_and_refused_bhs(self):
        """Assert for eligible for BHS, household is enrolled, and eligible for HTC since has refused BHS."""
        household_member = self.enroll_household()
        household_member = HouseholdMemberFactory(
            first_name='ERIK',
            initials='EXW',
            age_in_years=64,
            study_resident='Yes',
            household_structure=household_member.household_structure)

        household_member.member_status = REFUSED
        household_member.save(update_fields=['member_status'])

        self.assertEqual(household_member.member_status, REFUSED)
        subject_refusal = SubjectRefusalFactory(household_member=household_member)
        self.assertEqual(subject_refusal.household_member.member_status, HTC_ELIGIBLE)
        self.assertTrue(subject_refusal.household_member.refused)
        self.assertTrue(subject_refusal.household_member.eligible_htc)
        options = [BHS_SCREEN, HTC_ELIGIBLE]
        options.append(subject_refusal.household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = subject_refusal.household_member.member_status_choices
        self.assertEqual(x, member_status_choices)

    def test_refused_bhs_and_consent_later(self):
        """Assert for refused BHS, household not enrolled and BHS_SCREEN still available as option."""
        household_member = HouseholdMemberFactory(
            first_name='ERIK',
            initials='EXW',
            age_in_years=64,
            study_resident='Yes',
            household_structure=self.household_structure)
        household_member.member_status = REFUSED
        household_member.save(update_fields=['member_status'])
        self.assertEqual(household_member.member_status, REFUSED)
        subject_refusal = SubjectRefusalFactory(household_member=household_member)
        self.assertEqual(subject_refusal.household_member.member_status, HTC_ELIGIBLE)
        self.assertTrue(subject_refusal.household_member.refused)
        options = [BHS_SCREEN]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
        self.assertEqual(x, member_status_choices)

    def test_eligible_bhs(self):
        """Assert for eligible for BHS, household enrolled."""
        self.enroll_household()
        household_member = HouseholdMemberFactory(
            first_name='ERIK',
            initials='EXW',
            age_in_years=64,
            study_resident='Yes',
            household_structure=self.household_structure)
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
        options = [BHS, BHS_ELIGIBLE, DECEASED, REFUSED]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        x = household_member.member_status_choices
        self.assertEqual(x, member_status_choices)

    def test_consented(self):
        """Assert only returns BHS if member is consented."""
        household_member = self.enroll_household()
        self.assertTrue(household_member.is_consented)
        options = [BHS]
        options.append(household_member.member_status)
        options = list(set(options))
        options.sort()
        member_status_choices = [(item, item) for item in options]
        self.assertEqual(household_member.member_status_choices, member_status_choices)
