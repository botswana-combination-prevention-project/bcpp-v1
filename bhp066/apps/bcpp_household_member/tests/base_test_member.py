from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.core.bhp_variables.models import StudySite
from edc_constants.constants import NOT_APPLICABLE

from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household_member.tests.factories import (HouseholdMemberFactory, EnrollmentChecklistFactory)
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory

from ..constants import BHS, BHS_ELIGIBLE, BHS_SCREEN


class BaseTestMember(TestCase):

    household_member = None
    subject_consent = None
    enrollment_checklist = None
    registered_subject = None
    study_site = None
    household_structure = None
    representative_eligibility = None

    def setUp(self):

        from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration

        self.household_structure = None
        self.registered_subject = None
        self.representative_eligibility = None
        self.study_site = None
        self.intervention = None

        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        site_mappers.autodiscover()
        # set current community manually (not from settings)
        site_mappers.current_community = 'test_community'
        BcppAppConfiguration.study_start_datetime = datetime.today() + relativedelta(days=-2)
        BcppAppConfiguration.study_end_datetime = datetime.today() + relativedelta(days=45)
        bcpp_app_configuration = BcppAppConfiguration()
        # bypass any check of site_code and community against settings
        bcpp_app_configuration.confirm_site_code_in_settings = False
        bcpp_app_configuration.confirm_community_in_settings = False
        bcpp_app_configuration.prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        plot = PlotFactory(community='test_community',
                           household_count=1,
                           status='residential_habitable')
        household = Household.objects.get(plot=plot)
        self.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        self.representative_eligibility = RepresentativeEligibilityFactory(household_structure=self.household_structure)
        self.study_site = StudySite.objects.get(site_code=site_mappers.get_mapper(site_mappers.current_community).map_code)
        self.intervention = site_mappers.get_mapper(site_mappers.current_community).intervention

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
