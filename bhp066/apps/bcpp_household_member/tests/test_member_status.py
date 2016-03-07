from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.conf import settings

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.core.bhp_variables.models import StudySite
from edc_constants.constants import NOT_APPLICABLE, ALIVE, DEAD

from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.models import (HouseholdMember, SubjectAbsentee, EnrollmentChecklist,
                                                      EnrollmentLoss, SubjectDeath)
from bhp066.apps.bcpp_household_member.tests.factories import (HouseholdMemberFactory, EnrollmentChecklistFactory,
                                                               SubjectRefusalFactory, SubjectHtcFactory)
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory

from ..exceptions import MemberStatusError
from ..constants import (ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC_ELIGIBLE, NOT_ELIGIBLE, REFUSED, HTC, REFUSED_HTC,
                         DECEASED)


class TestMemberStatus(TestCase):

    household_member = None
    subject_consent = None
    enrollment_checklist = None
    registered_subject = None
    study_site = None
    household_structure = None
    representative_eligibility = None

    def setUp(self):

        from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
        site_mappers.autodiscover()
        from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
        self.household_structure = None
        self.registered_subject = None
        self.representative_eligibility = None
        self.study_site = None
        self.intervention = None
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.intervention = site_mappers.get_mapper(site_mappers.current_community).intervention
        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        self.survey = Survey.objects.get(survey_name='BCPP Year 2')  # see app_configuration
        plot = PlotFactory(community=settings.CURRENT_COMMUNITY, household_count=1, status='residential_habitable')
        self.household = Household.objects.get(plot=plot)
        self.household_structure = HouseholdStructure.objects.get(household=self.household, survey=self.survey1)
        self.representative_eligibility = RepresentativeEligibilityFactory(household_structure=self.household_structure)
        self.study_site = StudySite.objects.get(
            site_code=site_mappers.get_mapper(site_mappers.current_community).map_code)

    def enroll_household(self, household_member=None):
        if not household_member:
            household_member = HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=18,
                                                      present_today='Yes', study_resident='Yes',
                                                      household_structure=self.household_structure,
                                                      inability_to_participate=NOT_APPLICABLE)
        self.assertEquals(household_member.member_status, BHS_SCREEN)
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            report_datetime=datetime.today(),
            gender='M',
            dob=date.today() - relativedelta(years=18),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes')
        household_member = HouseholdMember.objects.get(pk=enrollment_checklist.household_member.pk)
        self.assertEquals(household_member.member_status, BHS_ELIGIBLE)
        from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
        subject_consent = SubjectConsentFactory(
            household_member=household_member,
            registered_subject=household_member.registered_subject,
            first_name=household_member.first_name,
            last_name='WERIK',
            gender=household_member.gender,
            dob=date.today() - relativedelta(years=18),
            initials=household_member.initials,
            study_site=self.study_site,
        )
        household_member = HouseholdMember.objects.get(pk=subject_consent.household_member.pk)
        self.household_structure = household_member.household_structure
        self.assertEquals(household_member.member_status, BHS)
        self.assertTrue(self.household_structure.enrolled)
        self.assertTrue(self.household_structure.household.enrolled)
        self.assertTrue(self.household_structure.household.plot.bhs)
        return household_member

    def test_household_member1(self):
        """Assert not reported based on age and residency"""
        HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EW', age_in_years=64,
                               study_resident='Yes', household_structure=self.household_structure)
        household_member = HouseholdMember.objects.get(household_structure=self.household_structure)
        self.assertEqual(household_member.member_status, BHS_SCREEN)

    def test_household_member1a(self):
        """Assert not reported based on age and residency, household not enrolled"""
        HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EW', age_in_years=64,
                               study_resident='No', household_structure=self.household_structure)
        if self.intervention:
            self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)
        else:
            self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, HTC_ELIGIBLE)

    def test_household_member2(self):
        """Assert not reported based on age and residency, household not enrolled"""
        household_member = HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EW',
                                                  age_in_years=75, study_resident='Yes', household_structure=self.household_structure)
        self.assertFalse(household_member.eligible_member)
        if self.intervention:
            self.assertFalse(household_member.eligible_htc)
            self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)
        else:
            self.assertTrue(household_member.eligible_htc)
            self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, HTC_ELIGIBLE)

    def test_household_member2a(self):
        """Assert not reported based on age and residency, household not enrolled"""
        HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EW', age_in_years=75,
                               study_resident='No', household_structure=self.household_structure)
        if self.intervention:
            self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)
        else:
            self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, HTC_ELIGIBLE)

    def test_household_member3(self):
        """Assert not eligible based on age and residency"""
        HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EW', age_in_years=15,
                               study_resident='Yes', household_structure=self.household_structure)
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)

    def test_household_member3a(self):
        """Assert not eligible based on age and residency"""
        HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EW', age_in_years=15,
                               study_resident='No', household_structure=self.household_structure)
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)

    def test_household_member4(self):
        """Assert not reported based on age and residency"""
        HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EW', age_in_years=16, study_resident='Yes',
                               household_structure=self.household_structure)
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, BHS_SCREEN)

    def test_household_member5(self):
        """Assert not reported based on age and residency"""
        HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EW', age_in_years=16,
                               study_resident='No', household_structure=self.household_structure)
        if self.intervention:
            self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, NOT_ELIGIBLE)
        else:
            self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, HTC_ELIGIBLE)

    def test_enrolled_household(self):
        """Assert household is enrolled when subject consents"""
        household_member = self.enroll_household()
        self.assertTrue(household_member.household_structure.enrolled)

    def test_consented(self):
        household_member = self.enroll_household()
        self.assertEqual(household_member.member_status, BHS)

    def test_enrolled_household1(self):
        """Assert is HTC eligible if not BHS eligible based on residency and household is enrolled"""
        household_member = self.enroll_household()
        household_member = HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EXW', age_in_years=64,
                                                  study_resident='No', household_structure=household_member.household_structure)
        self.assertFalse(household_member.eligible_member)
        self.assertFalse(household_member.enrollment_loss_completed)
        self.assertTrue(household_member.eligible_htc)
        self.assertEqual(HouseholdMember.objects.get(initials='EXW', household_structure=household_member.household_structure).member_status, HTC_ELIGIBLE)

    def test_enrolled_household2(self):
        """Assert is HTC eligible if not BHS eligible based on age (adult) and household is enrolled"""
        household_member = self.enroll_household()
        household_structure = HouseholdMember.objects.get(household_structure=household_member.household_structure).household_structure
        household_member = HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EXW',
                                                  age_in_years=75, study_resident='Yes', household_structure=household_structure)
        self.assertFalse(household_member.eligible_member)
        self.assertTrue(household_member.eligible_htc)
        self.assertEqual(HouseholdMember.objects.get(initials='EXW', household_structure=household_structure).member_status, HTC_ELIGIBLE)

    def test_enrolled_household3(self):
        """Assert is HTC eligible if not BHS eligible based on age (adult) and residency and household is enrolled"""
        household_member = self.enroll_household()
        household_structure = HouseholdMember.objects.get(household_structure=household_member.household_structure).household_structure
        HouseholdMemberFactory(inability_to_participate=NOT_APPLICABLE, first_name='ERIK', initials='EXW', age_in_years=75,
                               study_resident='No', household_structure=household_structure)
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
        """Asserts that an eligible member not present today is automatically creates a SubjectAbsentee."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',
            study_resident='Yes')
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, ABSENT)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=household_member).count(), 1)

    def test_absent_for_underage_household_member(self):
        """Asserts that an eligible member not present today is automatically creates a SubjectAbsentee."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=15,
            present_today='No',
            study_resident='Yes')
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, NOT_ELIGIBLE)
        household_member.age_in_years = 20
        household_member.save()
        self.assertEqual(household_member.member_status, ABSENT)
        household_member.inability_to_participate = 'Deaf/Mute'
        household_member.save()
        self.assertEqual(household_member.member_status, NOT_ELIGIBLE)

    def test_change_household_member1(self):
        """Asserts that an eligible member present today but then set to no present today is  BHS_SCREEN"""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        household_member.present_today = 'No'
        household_member.save()
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, BHS_SCREEN)

        # simulate user changes status on participation view
        household_member.member_status = ABSENT
        household_member.save(update_fields=['member_status'])

        self.assertEqual(SubjectAbsentee.objects.filter(household_member=household_member).count(),
                         1, 'Expected 1 SubjectAbsentee instance.')
        self.assertEqual(HouseholdMember.objects.get(household_structure=self.household_structure).member_status, ABSENT)
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        household_member.modified = household_member.created + timedelta(seconds=30)
        household_member.member_status = BHS_SCREEN
        household_member.save(update_fields=['member_status'])
        self.assertEqual(household_member.member_status, BHS_SCREEN)

    def test_change_household_member2(self):
        """Asserts that an eligible member not present today is automatically ABSENT"""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',
            study_resident='Yes')
        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        self.assertEquals(household_member.member_status, ABSENT)

    def test_change_household_member2a(self):
        """Asserts that an eligible member not present today must manually set member_status to BHS_SCREEN before filling eligibility"""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',
            study_resident='Yes')
        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        self.assertRaisesRegexp(
            MemberStatusError,
            BHS_SCREEN,
            EnrollmentChecklistFactory,
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=50),
            initials=household_member.initials,
            part_time_resident='Yes')

    def test_change_household_member3(self):
        """Asserts that an eligible member who is not present yesterday can later be BHS ELIGIBLE."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='No',
            study_resident='Yes')
        self.assertTrue(household_member.reported)
        self.assertEquals(household_member.member_status, ABSENT)
        household_member.member_status = BHS_SCREEN  # this would be changed by the user
        household_member.save(update_fields=['member_status'])

        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            report_datetime=datetime.today(),
            gender='M',
            dob=date.today() - relativedelta(years=50),
            initials=household_member.initials,
            part_time_resident='Yes')
        self.assertTrue(enrollment_checklist.is_eligible)
        self.assertTrue(enrollment_checklist.household_member.eligible_subject)
        self.assertEquals(enrollment_checklist.household_member.member_status, BHS_ELIGIBLE)

    def test_change_household_member4(self):
        """Asserts that an eligible member can set member status to REFUSED."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')

        household_member.member_status = REFUSED
        household_member.save(update_fields=['member_status'])

        self.assertEqual(household_member.member_status, REFUSED)
        self.assertFalse(household_member.refused)

    def test_change_deceased_member(self):
        """Asserts that a household member can switch between DESEASED and BHS_MEMBER."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.member_status, BHS_SCREEN)
        self.assertEqual(household_member.survival_status, ALIVE)
        self.assertTrue(household_member.eligible_member)
        self.assertEqual(SubjectDeath.objects.all().count(), 0)

        household_member.member_status = DECEASED
        household_member.save(update_fields=['member_status'])
        household_member = HouseholdMember.objects.get(pk=pk)
        self.assertEqual(household_member.survival_status, DEAD)
        self.assertEqual(household_member.present_today, 'No')
        self.assertFalse(household_member.eligible_member)
        self.assertFalse(household_member.absent)
        self.assertEqual(household_member.member_status, DECEASED)

    def test_change_household_member5(self):
        """Asserts that an eligible member that refuses before eligibility is REFUSED."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        household_member.member_status = REFUSED
        household_member.save(update_fields=['member_status'])
        household_member = HouseholdMember.objects.get(pk=pk)
        SubjectRefusalFactory(household_member=household_member)
        if self.intervention:
            self.assertEqual(household_member.member_status, REFUSED)
            self.assertTrue(household_member.refused)
        else:
            self.assertEqual(household_member.member_status, HTC_ELIGIBLE)
            self.assertTrue(household_member.refused)

    def test_change_household_member6(self):
        """Asserts that an eligible member that fails Eligibility is NOT ELIGIBLE if the household is not enrolled."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            report_datetime=datetime.today(),
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes',
            has_identity='No')
        self.assertFalse(enrollment_checklist.household_member.eligible_subject)
        if self.intervention:
            self.assertFalse(enrollment_checklist.household_member.eligible_htc)
            self.assertEquals(enrollment_checklist.household_member.member_status, NOT_ELIGIBLE)
        else:
            self.assertTrue(enrollment_checklist.household_member.eligible_htc)
            self.assertEquals(enrollment_checklist.household_member.member_status, HTC_ELIGIBLE)

    def test_member_refusing_htc_failed_eligibility(self):
        """Asserts that an eligible member that fails Eligibility but becomes HTC_ELIGIBLE as household is enrolled
        then however refuses htc to end up with status REFUSED_HTC."""
        household_member = self.enroll_household()
        household_member = HouseholdMemberFactory(
            household_structure=household_member.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        # add a member that is NOT eligible for BHS
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes',
            has_identity='No')
        self.assertFalse(enrollment_checklist.household_member.eligible_subject)
        self.assertTrue(enrollment_checklist.household_member.eligible_htc)  # false because no refusal
        self.assertEquals(enrollment_checklist.household_member.member_status, HTC_ELIGIBLE)

        subject_htc = SubjectHtcFactory(household_member=enrollment_checklist.household_member)
        self.assertEquals(subject_htc.household_member.member_status, HTC)

        subject_htc.accepted = 'No'
        subject_htc.save()
        self.assertEquals(subject_htc.household_member.member_status, REFUSED_HTC)

        subject_htc.accepted = 'Yes'
        subject_htc.save()
        self.assertEquals(subject_htc.household_member.member_status, HTC)

    def test_can_consent_member_in_yr2(self):
        """Asserts that a member member that was not consented year one can now be consented in y2."""
        household_member = self.enroll_household()
        HouseholdMemberFactory(
            household_structure=household_member.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        # Now add a year2 household member
        year2_survey = Survey.objects.get(survey_slug='bcpp-year-2')
        year2_structure = HouseholdStructure.objects.get(survey=year2_survey, household=self.household)
        # Representative eligibility
        RepresentativeEligibilityFactory(
            household_structure=year2_structure)
        household_member_y2 = HouseholdMemberFactory(
            household_structure=year2_structure,
            gender='M',
            age_in_years=21,
            present_today='Yes',
            study_resident='Yes')
        # Fill an enrollment checklist for the year two household member
        self.assertEquals(household_member_y2.member_status, BHS_SCREEN)
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member_y2,
            gender='M',
            dob=date.today() - relativedelta(years=21),
            guardian='No',
            initials=household_member_y2.initials,
            part_time_resident='Yes',
            has_identity='Yes')
        self.assertEquals(household_member_y2.member_status, BHS_ELIGIBLE)
        self.assertTrue(enrollment_checklist.household_member.eligible_subject)

    def test_member_refusing_htc_after_refusing_bhs(self):
        """Asserts that an eligible member that refuses BHS but household is enrolled
            then however refuses htc to end up with status REFUSED_HTC."""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        self.enroll_household()
        household_member = HouseholdMember.objects.get(pk=household_member.pk)

        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        self.assertEquals(household_member.member_status, BHS_SCREEN)
        household_member.member_status = REFUSED
        household_member.save(update_fields=['member_status'])
        subject_refusal = SubjectRefusalFactory(household_member=household_member)
        self.assertFalse(subject_refusal.household_member.eligible_subject)
        self.assertTrue(subject_refusal.household_member.eligible_htc)
        self.assertEquals(subject_refusal.household_member.member_status, HTC_ELIGIBLE)

        subject_htc = SubjectHtcFactory(household_member=subject_refusal.household_member)
        self.assertEquals(subject_htc.household_member.member_status, HTC)

        subject_htc.accepted = 'No'
        subject_htc.save()
        self.assertEquals(subject_htc.household_member.member_status, REFUSED_HTC)

        subject_htc.accepted = 'Yes'
        subject_htc.save()
        self.assertEquals(subject_htc.household_member.member_status, HTC)

    def test_change_household_member6a(self):
        """Start as Eligible and edit eligibility checklist to switch to Not Eligible"""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes',
            has_identity='Yes')
        self.assertTrue(enrollment_checklist.household_member.eligible_subject)
        self.assertFalse(enrollment_checklist.household_member.eligible_htc)
        self.assertEquals(enrollment_checklist.household_member.member_status, BHS_ELIGIBLE)
        self.assertEqual(EnrollmentLoss.objects.filter(household_member=enrollment_checklist.household_member).count(), 0)
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=enrollment_checklist.household_member)
        enrollment_checklist.has_identity = 'No'
        enrollment_checklist.save()
        self.assertFalse(enrollment_checklist.household_member.eligible_subject)
        self.assertFalse(household_member.household_structure.household.plot.bhs)
        if self.intervention:
            self.assertFalse(enrollment_checklist.household_member.eligible_htc)
            self.assertEquals(enrollment_checklist.household_member.member_status, NOT_ELIGIBLE)
        else:
            self.assertTrue(enrollment_checklist.household_member.eligible_htc)
            self.assertEquals(enrollment_checklist.household_member.member_status, HTC_ELIGIBLE)
        self.assertEqual(EnrollmentLoss.objects.filter(household_member=household_member).count(), 1)

    def test_change_household_member6b(self):
        """Start as Not Eligible and edit eligibility checklist to switch to Bhs Eligible"""
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        self.assertEquals(household_member.member_status, BHS_SCREEN)
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes',
            has_identity='No')
        self.assertFalse(enrollment_checklist.household_member.eligible_subject)
        self.assertTrue(enrollment_checklist.household_member.enrollment_checklist_completed)
        self.assertTrue(enrollment_checklist.household_member.enrollment_loss_completed)
        self.assertFalse(enrollment_checklist.household_member.refused)
        if self.intervention:
            # This is in CPC(Plot should be enrolled for 1 to be HTC_ELIGIBLE)
            self.assertFalse(enrollment_checklist.household_member.eligible_htc)
            self.assertEquals(enrollment_checklist.household_member.member_status, NOT_ELIGIBLE)
        else:
            # This is in CPC(Plot should be enrolled for 1 to be HTC_ELIGIBLE)
            self.assertTrue(enrollment_checklist.household_member.eligible_htc)
            self.assertEquals(enrollment_checklist.household_member.member_status, HTC_ELIGIBLE)
        self.assertEqual(EnrollmentLoss.objects.filter(household_member=enrollment_checklist.household_member).count(), 1)
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        enrollment_checklist.has_identity = 'Yes'
        enrollment_checklist.save()
        self.assertTrue(enrollment_checklist.household_member.eligible_subject)
        self.assertFalse(enrollment_checklist.household_member.eligible_htc)
        self.assertEquals(enrollment_checklist.household_member.member_status, BHS_ELIGIBLE)
        self.assertEqual(EnrollmentLoss.objects.filter(household_member=enrollment_checklist.household_member).count(), 0)

    def test_change_household_member7(self):
        """Assert enrolling a household_structure updates the member status of other members in the household."""
        household_member1 = HouseholdMemberFactory(
            household_structure=self.household_structure,  # intervention = True
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        household_member2 = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=25,
            present_today='Yes',
            study_resident='Yes')
        # both default to BHS_SCREEN
        self.assertEquals(household_member1.member_status, BHS_SCREEN)
        self.assertEquals(household_member2.member_status, BHS_SCREEN)
        enrollment_checklist1 = EnrollmentChecklistFactory(
            household_member=household_member1,
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member1.initials,
            part_time_resident='Yes',
            has_identity='No')
        household_member1 = HouseholdMember.objects.get(pk=enrollment_checklist1.household_member.pk)
        self.assertFalse(household_member1.household_structure.household.plot.bhs)
        if self.intervention:
            # This is in CPC(Plot should be enrolled for 1 to be HTC_ELIGIBLE)
            self.assertEquals(household_member1.member_status, NOT_ELIGIBLE)
        else:
            # This is in ECC(Plot does not need to be enrolled for 1 to be HTC_ELIGIBLE)
            self.assertEquals(household_member1.member_status, HTC_ELIGIBLE)
        enrollment_checklist2 = EnrollmentChecklistFactory(
            household_member=household_member2,
            gender='M',
            dob=date.today() - relativedelta(years=25),
            guardian='No',
            initials=household_member2.initials,
            part_time_resident='Yes',
            has_identity='Yes')
        household_member2 = HouseholdMember.objects.get(pk=enrollment_checklist2.household_member.pk)
        # 2 is eligible
        self.assertEquals(household_member2.member_status, BHS_ELIGIBLE)
        from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
        subject_consent = SubjectConsentFactory(
            household_member=enrollment_checklist2.household_member,
            registered_subject=household_member2.registered_subject,
            first_name=household_member2.first_name,
            last_name='WERIK',
            gender=household_member2.gender,
            dob=date.today() - relativedelta(years=25),
            initials=household_member2.initials,
            study_site=self.study_site,)
        # 2 has consented, so BHS
        self.assertEquals(subject_consent.household_member.member_status, BHS)
        household_member2 = HouseholdMember.objects.get(pk=subject_consent.household_member.pk)
        self.assertEquals(household_member2.member_status, BHS)
        # because 2 consented, household is enrolled
        self.assertTrue(household_member2.household_structure.enrolled)
        self.assertTrue(household_member2.household_structure.household.enrolled)

        household_member1 = HouseholdMember.objects.get(pk=household_member1.pk)
        if self.intervention:
            # This is in CPC(Plot should be enrolled for 1 to be HTC_ELIGIBLE)
            # since household is enrolled, 1 is now HTC_ELIGIBLE in CPC
            self.assertEquals(household_member1.member_status, HTC_ELIGIBLE)
        else:
            # This is in ECC(Plot does not need to be enrolled for 1 to be HTC_ELIGIBLE)
            # household is now enrolled, 1 remains HTC_ELIGIBLE
            self.assertEquals(household_member1.member_status, HTC_ELIGIBLE)

    def test_change_household_member8(self):
        """Asserts that an eligible member in a household that is enrolled AFTER the member was added and who fails eligibility is HTC ELIGIBLE."""
        household_member = self.enroll_household()
        household_member = HouseholdMemberFactory(
            household_structure=household_member.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes',
            has_identity='No')
        household_member = HouseholdMember.objects.get(pk=enrollment_checklist.household_member.pk)
        self.assertFalse(household_member.eligible_subject)
        self.assertTrue(household_member.enrollment_checklist_completed)
        self.assertFalse(household_member.refused)
        self.assertTrue(household_member.eligible_htc)
        self.assertEquals(household_member.member_status, HTC_ELIGIBLE)

    def test_change_household_member10(self):
        self.enroll_household()
        self.assertTrue(self.household_structure.enrolled)
        self.assertTrue(self.household_structure.household.enrolled)
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        self.assertTrue(self.household_structure.enrolled)
        self.assertTrue(self.household_structure.household.enrolled)
        self.assertTrue(household_member.plot_enrolled)
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes',
            has_identity='Yes')
        household_member = HouseholdMember.objects.get(pk=enrollment_checklist.household_member.pk)
        self.assertTrue(household_member.eligible_subject)
        self.assertTrue(household_member.enrollment_checklist_completed)
        self.assertFalse(household_member.refused)
        self.assertFalse(household_member.eligible_htc)
        self.assertEquals(household_member.member_status, BHS_ELIGIBLE)

        # simulate user change using particiherpation view
        household_member = HouseholdMember.objects.get(pk=enrollment_checklist.household_member.pk)
        household_member.member_status = REFUSED
        household_member.save(update_fields=['member_status'])
        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        self.assertEquals(household_member.member_status, REFUSED)
        # member_status remains as REFUSED until refusal_log is filled.
        subject_refusal = SubjectRefusalFactory(household_member=household_member)
        household_member = HouseholdMember.objects.get(pk=subject_refusal.household_member.pk)
        self.assertFalse(household_member.enrollment_checklist_completed)
        self.assertTrue(household_member.refused)
        self.assertFalse(household_member.eligible_subject)
        self.assertTrue(household_member.eligible_htc)
        self.assertEquals(household_member.member_status, HTC_ELIGIBLE)

    def test_change_household_member11(self):
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')

        household_member.member_status = BHS_SCREEN
        household_member.save(update_fields=['member_status'])

        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes',
            has_identity='Yes')
        household_member = HouseholdMember.objects.get(pk=enrollment_checklist.household_member.pk)
        self.assertTrue(household_member.eligible_subject)
        self.assertTrue(household_member.enrollment_checklist_completed)
        self.assertFalse(household_member.refused)
        self.assertFalse(household_member.eligible_htc)
        self.assertEquals(household_member.member_status, BHS_ELIGIBLE)

        # simulate user change through participation view
        household_member.member_status = REFUSED
        household_member.save(update_fields=['member_status'])
        household_member = HouseholdMember.objects.get(pk=enrollment_checklist.household_member.pk)
        self.assertEquals(household_member.member_status, REFUSED)

        subject_refusal = SubjectRefusalFactory(household_member=household_member)
        household_member = HouseholdMember.objects.get(pk=subject_refusal.household_member.pk)
        if self.intervention:
            self.assertEquals(household_member.member_status, REFUSED)
            self.assertFalse(household_member.eligible_subject)
            self.assertFalse(household_member.enrollment_checklist_completed)
            self.assertTrue(household_member.refused)
            self.assertFalse(household_member.eligible_htc)
        else:
            self.assertEquals(household_member.member_status, HTC_ELIGIBLE)
            self.assertFalse(household_member.eligible_subject)
            self.assertFalse(household_member.enrollment_checklist_completed)
            self.assertTrue(household_member.refused)
            self.assertTrue(household_member.eligible_htc)

    def test_member_htc_to_htc_eligible(self):
        """Asserts that an eligible member in a household that is enrolled AFTER the member was added and who fails eligibility is HTC ELIGIBLE."""
        household_member = self.enroll_household()
        household_member = HouseholdMemberFactory(
            household_structure=household_member.household_structure,
            gender='M',
            age_in_years=20,
            present_today='Yes',
            study_resident='Yes')
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=20),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes',
            has_identity='No')
        household_member = HouseholdMember.objects.get(pk=enrollment_checklist.household_member.pk)
        self.assertFalse(household_member.eligible_subject)
        self.assertTrue(household_member.enrollment_checklist_completed)
        self.assertFalse(household_member.refused)
        self.assertTrue(household_member.eligible_htc)
        # A member that is HTC_ELIGIBLE can still be enrolled in to full BHS
        self.assertEquals(household_member.member_status, HTC_ELIGIBLE)
        # Perform HTC on a subject
        subject_htc = SubjectHtcFactory(
            household_member=household_member)
        household_member = HouseholdMember.objects.get(pk=subject_htc.household_member.pk)
        self.assertTrue(household_member.htc)
        self.assertEquals(household_member.member_status, HTC)
        # Come back from HTC to HTC_ELIGIBLE which means you can enroll the member in to BHS in the case that they have now
        # agreed to fully participate
        household_member.member_status = BHS_SCREEN
        household_member.save(update_fields=['member_status'])
        self.assertFalse(household_member.eligible_htc)
        self.assertEquals(household_member.member_status, BHS_SCREEN)
