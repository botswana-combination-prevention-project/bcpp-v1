from django.test import TestCase

from edc.map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from bhp066.apps.bcpp_household.models import HouseholdStructure, Household
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule

from ..classes import HouseholdDashboard


class TestDashboard(TestCase):

    app_label = 'testing'

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        site_mappers.autodiscover()
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        self.community = mapper().get_map_area()
        gps_degrees_s, gps_minutes_s, gps_degrees_e, gps_minutes_e = mapper().test_location
        self.plot = PlotFactory(community=self.community,
                                gps_degrees_s=gps_degrees_s,
                                gps_minutes_s=gps_minutes_s,
                                gps_degrees_e=gps_degrees_e,
                                gps_minutes_e=gps_minutes_e,
                                household_count=2,
                                status='residential_habitable')
        self.household1 = Household.objects.filter(plot=self.plot).order_by('created')[0]
        self.household_structure1 = HouseholdStructure.objects.get(household=self.household1, survey=self.survey1)
        self.household2 = Household.objects.filter(plot=self.plot).order_by('created')[1]
        self.household_member1 = HouseholdMemberFactory(household_structure=self.household_structure1,
                                                        age_in_years=26,
                                                        present_today='Yes',
                                                        member_status='RESEARCH')
        self.household_member2 = HouseholdMemberFactory(household_structure=self.household_structure1, age_in_years=36, present_today='Yes')
        self.household_member3 = HouseholdMemberFactory(household_structure=self.household_structure1, age_in_years=12, present_today='Yes')
        self.household_member4 = HouseholdMemberFactory(household_structure=self.household_structure1, age_in_years=99, present_today='Yes')
        self.dashboard_type = 'household'
        self.dashboard_model = 'household'
        self.dashboard_id = self.household1.pk

        self.household_member1.eligible_subject = True

        self.subject_consent = SubjectConsentFactory(
            household_member=self.household_member1,
            first_name=self.household_member1.first_name,
            initials=self.household_member1.initials,
            registered_subject=self.household_member1.registered_subject)

    def test_create_household_dashboard1(self):
        dashboard_type = 'household'
        dashboard_model = 'household'
        dashboard_id = self.household1.pk
        household_dashboard = HouseholdDashboard(dashboard_type, dashboard_id, dashboard_model)
        household_dashboard.set_context()

    def test_create_household_dashboard2(self):
        dashboard_type = 'household'
        dashboard_model = 'household_structure'
        dashboard_id = self.household_structure1.pk
        household_dashboard = HouseholdDashboard(dashboard_type, dashboard_id, dashboard_model)
        household_dashboard.set_context()
