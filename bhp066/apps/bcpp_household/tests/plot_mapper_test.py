from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase

from edc.map.classes import site_mappers, Mapper
from edc.map.exceptions import MapperError

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from ..forms import PlotForm
from ..models import Household, HouseholdStructure, HouseholdLog, HouseholdLogEntry, Plot

from .factories import PlotFactory, PlotLogEntryFactory


class TestPlotMapper(Mapper):
    map_area = 'test_community'
    map_code = '999'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.011111
    gps_center_lon = 25.741111
    radius = 5.5
    enhanced_care = True
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class PlotTests(TestCase):

    def setUp(self):
        SurveyFactory()

    def test_community_type(self):
        self.assertTrue(TestPlotMapper().enhanced_care)
