from datetime import datetime

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.map.classes import site_mappers, Mapper

from bhp066.apps.bcpp_household.helpers import ReplacementHelper
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry
from bhp066.apps.bcpp_household_member.constants import REFUSED, ABSENT
from bhp066.apps.bcpp_household_member.tests.factories import SubjectRefusalFactory, SubjectAbsenteeEntryFactory
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure, HouseholdLog, HouseholdLogEntry, HouseholdRefusal, HouseholdAssessment

from .factories import HouseholdFactory
from .factories import PlotFactory
from .factories import HouseholdRefusalFactory
from .factories import HouseholdLogFactory
from .factories import HouseholdLogEntryFactory
from .factories import HouseholdAssessmentFactory


class TestPlotMapper(Mapper):
    map_area = 'test_community12'
    map_code = '095'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()
site_mappers.register(TestPlotMapper)


class ReplacementTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration

    def test_replacement_plot1(self, **kwargs):
        plot = PlotFactory(
            community='test_community12',
            household_count=1,
            status='non_residential',
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=2,
            replaces='ERIK')
        replacement_helper = ReplacementHelper()
        self.assertEquals(replacement_helper.replaceable_plots(), [plot])

    def test_replacement_plot2(self, **kwargs):
        plot = PlotFactory(
            community='test_community12',
            household_count=0,
            status='non_residential',
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=2,
            replaces=None)
        replacement_helper = ReplacementHelper()
        self.assertEquals(replacement_helper.replaceable_plots(), [])

    def test_replacement_plot3(self, **kwargs):
        plot = PlotFactory(
            community='test_community12',
            household_count=1,
            status='residential_habitable',
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=2,
            replaces='H12345')
        replacement_helper = ReplacementHelper()
        self.assertEquals(replacement_helper.replaceable_plots(), [])
