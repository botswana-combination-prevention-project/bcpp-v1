from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase

from edc.map.classes import site_mappers, Mapper
from edc.map.exceptions import MapperError

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_survey.tests.factories import SurveyFactory

from ..forms import PlotForm
from ..models import Household, HouseholdStructure, HouseholdLog, HouseholdLogEntry, Plot
from edc.map.classes import site_mappers

from .factories import PlotFactory


class TestPlotMapper(Mapper):
    map_area = 'test_community'
    map_code = '999'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.011111
    gps_center_lon = 25.741111
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)

class PlotReplcamentMethodTests(TestCase):

    def setUp(self):
        SurveyFactory()

    def test_replace_refusal_plot(self):

        print "*********************************"
        print "refusal replacement"
        print "*****************************************"

        plot = PlotFactory(
                community='test_community', 
                household_count=1, 
                status='occupied', 
                eligible_members=3, 
                report_datetime=datetime.date.today(),
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.6666599,
                gps_degrees_e=25,
                gps_minutes_e=44.466660,
                selected=1,
                access_attempts=0,)
        household = Household.objects.filter(plot=plot)
        h_structure = HouseholdStructure.objects.get(household=household)
        members = HouseholdMember.objects.filter(household_structure=h_structure)

    def test_replacement_absentee(self):
        print "*********************************"
        print "Absentee replacement"
        print "*****************************************"

    def test_replacement_none_consented(self):

        print "*********************************"
        print "None Consented replacement"
        print "*****************************************"