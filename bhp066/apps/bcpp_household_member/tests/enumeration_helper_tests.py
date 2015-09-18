import pprint

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc_constants.constants import NOT_APPLICABLE
from edc.core.bhp_variables.models import StudySite
from edc.subject.visit_schedule.classes import site_visit_schedules

from bhp066.apps.bcpp.app_configuration.classes import bcpp_app_configuration
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_household.utils.survey_dates_tuple import SurveyDatesTuple

from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory

from ..constants import ABSENT, BHS, BHS_ELIGIBLE, BHS_SCREEN, HTC_ELIGIBLE, NOT_ELIGIBLE, REFUSED, UNDECIDED, ANNUAL
from ..exceptions import HouseholdStructureNotEnrolled


class EnumerationHelperTests(TestCase):

    def __init__(self, *args, **kwargs):
        self.household_member = None
        self.subject_consent = None
        self.enrollment_checklist = None
        self.registered_subject = None
        self.study_site = None
        self.subject_consent = None
        super(EnumerationHelperTests, self).__init__(*args, **kwargs)

    def setUp(self):
        site_mappers.autodiscover()

        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        mapper = site_mappers._registry_by_code.get('01')
        mapper.survey_dates = {
            'bcpp-year-1': SurveyDatesTuple(
                name='bhs',
                start_date=date.today() + relativedelta(years=-1) + relativedelta(days=-89),
                full_enrollment_date=date.today() + relativedelta(years=-1) + relativedelta(days=60),
                end_date=date.today() + relativedelta(years=-1) + relativedelta(days=89),
                smc_start_date=date.today() + relativedelta(years=-1) + relativedelta(days=89)),
            'bcpp-year-2': SurveyDatesTuple(
                name='t1',
                start_date=date.today() + relativedelta(years=0) + relativedelta(days=-89),
                full_enrollment_date=date.today() + relativedelta(years=0) + relativedelta(days=60),
                end_date=date.today() + relativedelta(years=0) + relativedelta(days=89),
                smc_start_date=date.today() + relativedelta(years=0) + relativedelta(days=89)),
        }

        bcpp_app_configuration.survey_setup = {
            'bcpp-year-1':
                {'survey_name': 'BCPP Year 1',
                 'survey_slug': 'bcpp-year-1',
                 'datetime_start': datetime.today() + relativedelta(years=-1) + relativedelta(days=-30),
                 'datetime_end': datetime.today() + relativedelta(years=-1) + relativedelta(days=30)},
            'bcpp-year-2':
                {'survey_name': 'BCPP Year 2',
                 'survey_slug': 'bcpp-year-2',
                 'datetime_start': datetime.today() + relativedelta(days=-90),
                 'datetime_end': datetime.today() + relativedelta(days=90)},
            'bcpp-year-3':
                {'survey_name': 'BCPP Year 3',
                 'survey_slug': 'bcpp-year-3',
                 'datetime_start': datetime.today() + relativedelta(years=1) + relativedelta(days=-30),
                 'datetime_end': datetime.today() + relativedelta(years=1) + relativedelta(days=30)},
        }

        bcpp_app_configuration.prepare()
        site_lab_tracker.autodiscover()
        site_visit_schedules.autodiscover()
        site_visit_schedules.build_all()

        self.survey2 = Survey.objects.current_survey()
        self.survey1 = Survey.objects.previous_survey()
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
        self.household = Household.objects.get(plot=plot)
        self.source_household_structure = HouseholdStructure.objects.get(household=self.household, survey=self.survey1)
        self.target_household_structure = HouseholdStructure.objects.get(household=self.household, survey=self.survey2)
        self.representative_eligibility = RepresentativeEligibilityFactory(household_structure=self.source_household_structure)
        self.study_site = StudySite.objects.get(site_code=site_mappers.get_current_mapper().map_code)
        self.intervention = site_mappers.get_current_mapper().intervention

        # add members to source
        HouseholdMemberFactory(household_structure=self.source_household_structure)
        HouseholdMemberFactory(household_structure=self.source_household_structure)
        HouseholdMemberFactory(household_structure=self.source_household_structure)
        HouseholdMemberFactory(household_structure=self.source_household_structure)
        HouseholdMemberFactory(household_structure=self.source_household_structure)

    def enroll_household(self):
        household_member = HouseholdMemberFactory(first_name='ERIK', initials='EW', age_in_years=18, study_resident='Yes', household_structure=self.source_household_structure)
        enrollment_checklist = EnrollmentChecklistFactory(
            household_member=household_member,
            gender='M',
            dob=date.today() - relativedelta(years=18),
            guardian='No',
            initials=household_member.initials,
            part_time_resident='Yes')
        from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
        self.subject_consent = SubjectConsentFactory(
            household_member=enrollment_checklist.household_member,
            first_name="ERIK",
            last_name='WERIK',
            gender='M',
            dob=date.today() - relativedelta(years=18),
            initials=household_member.initials,
            study_site=self.study_site,
            )
        self.assertEqual(self.subject_consent.household_member.member_status, BHS)
        self.assertTrue(self.subject_consent.household_member.household_structure.enrolled)
        return household_member

    def test_add_members_not_enrolled(self):
        """Assert members are NOT added if household is not enrolled."""
        # household_member = self.enroll_household()
        self.assertRaises(
            HouseholdStructureNotEnrolled,
            HouseholdStructure.objects.add_household_members_from_survey,
            self.household, self.survey1, self.survey2)

    def test_add_members_enrolled(self):
        """Assert members are added if household is enrolled."""
        self.enroll_household()
        household_structure = HouseholdStructure.objects.add_household_members_from_survey(
            self.household, self.survey1, self.survey2)
        self.assertEqual(HouseholdMember.objects.filter(household_structure=household_structure).count(), 0)

    def test_add_members_enrolled_as_annual(self):
        """Assert members are added if household is not enrolled."""
        self.enroll_household()  # one member is consented
        HouseholdStructure.objects.add_household_members_from_survey(
            self.household, self.survey1, self.survey2)
        household_structure = HouseholdStructure.objects.get(
            household=self.household,
            survey=self.survey2)
        self.assertEquals(HouseholdMember.objects.filter(
            internal_identifier=self.subject_consent.household_member.internal_identifier,
            household_structure__survey=self.survey2).count(), 1)
        member = HouseholdMember.objects.get(
            internal_identifier=self.subject_consent.household_member.internal_identifier,
            household_structure__survey=self.survey2)
        self.assertEqual(HouseholdMember.objects.filter(
            household_structure=household_structure,
            member_status=ANNUAL).count(), 1)

    def test_add_members_count(self):
        """Assert members are added if household is not enrolled."""
        self.enroll_household()
        HouseholdStructure.objects.add_household_members_from_survey(
            self.household, self.survey1, self.survey2)
        self.assertEqual(
            HouseholdMember.objects.filter(household_structure=self.target_household_structure).count(),
            HouseholdMember.objects.filter(household_structure=self.source_household_structure).count()
            )

    def test_add_members_aged_in_and_out(self):
        """Assert members ageing in and out are correctly set to eligible/not eligible."""
        self.enroll_household()
        age_in = HouseholdMemberFactory(household_structure=self.source_household_structure,
                                        age_in_years=15,
                                        study_resident='Yes',
                                        inability_to_participate=NOT_APPLICABLE)
        age_out = HouseholdMemberFactory(household_structure=self.source_household_structure,
                                         age_in_years=64,
                                         study_resident='Yes',
                                         inability_to_participate=NOT_APPLICABLE)
        HouseholdStructure.objects.add_household_members_from_survey(
            self.household, self.survey1, self.survey2)
        age_out = HouseholdMember.objects.get(
            internal_identifier=age_out.internal_identifier, household_structure=self.target_household_structure)
        self.assertFalse(age_out.eligible_member)
        age_in = HouseholdMember.objects.get(
            internal_identifier=age_in.internal_identifier, household_structure=self.target_household_structure)
        self.assertTrue(age_in.eligible_member)
