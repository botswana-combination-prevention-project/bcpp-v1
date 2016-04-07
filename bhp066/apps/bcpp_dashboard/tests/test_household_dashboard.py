from django.test import TestCase
from django.test.utils import override_settings


from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.map.classes import Mapper, site_mappers

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_household.models.household_log import HouseholdLog
from bhp066.apps.bcpp_dashboard.classes.household_dashboard import HouseholdDashboard


class TestHouseholdDashboard(TestCase):
    community = 'test_community'

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()

    def test_household_log_create(self):
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')
        household_structures = HouseholdStructure.objects.filter(household__plot=plot)
        household_logs = HouseholdLog.objects.filter(household_structure__in=household_structures)
        household_logs.delete()
        household_dashboard = HouseholdDashboard()
        household_dashboard._household_structure = household_structures[0]
        household_dashboard.household_log
        self.assertTrue(household_dashboard.household_log)
