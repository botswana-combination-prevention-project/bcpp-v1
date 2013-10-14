from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.conf import settings

from edc.map.classes import site_mappers, Mapper

from apps.bcpp_survey.tests.factories import SurveyFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_household_member.models import HouseholdMember

from ..classes  import PlotIdentifier
from ..models import PlotIdentifierHistory, Household, HouseholdStructure, HouseholdLog, HouseholdLogEntry, Plot
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


class PlotTests(TestCase):

    def setUp(self):
        SurveyFactory()

    def test_plot_creates_household1(self):
        """if you create a plot as occupied, should create one household."""

        plot = PlotFactory(community='test_community', household_count=1, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)

    def test_plot_creates_household2(self):
        """if you create a plot with two households should create two households."""
        plot = PlotFactory(community='test_community', household_count=2, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_plot_creates_household3(self):
        """if you change a plot by adding a second households should create another household."""
        plot = PlotFactory(community='test_community', household_count=1, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)
        plot.household_count = 2
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_plot_creates_household4(self):
        """if you create a plot as None, should create one household."""
        plot = PlotFactory(community='test_community', household_count=0, status=None)
        self.assertEqual(Household.objects.filter(plot=plot).count(), 0)

    def test_plot_deletes_household1(self):
        """if you change a plot by subtracting a household should delete last created household."""
        plot = PlotFactory(community='test_community', household_count=2, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)

    def test_plot_deletes_household2(self):
        """if you change a plot by subtracting a household should delete last created household."""
        plot = PlotFactory(community='test_community', household_count=2, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 2)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 2)
        for household_log in HouseholdLog.objects.filter(household_structure__household__plot=plot):
            HouseholdLogEntry.objects.create(household_log=household_log, report_datetime=datetime.today())
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 2)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 2)

    def test_plot_deletes_household3(self):
        """if you create 3 plots, add log entries for two and change the plot by subtracting two households, should delete one."""
        #create a plot with 3 households
        plot = PlotFactory(community='test_community', household_count=3, status='occupied')
        # assert household, household structure and an empty log are created
        self.assertEqual(Household.objects.filter(plot=plot).count(), 3)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 3)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 3)
        # create a log entry for two households
        for index, household_log in enumerate(HouseholdLog.objects.filter(household_structure__household__plot=plot)):
            if not index == 0:
                HouseholdLogEntry.objects.create(household_log=household_log, report_datetime=datetime.today())
        self.assertEqual(HouseholdLogEntry.objects.filter(household_log__household_structure__household__plot=plot).count(), 2)
        # change the number of household to 2
        plot.household_count = 2
        plot.save()
        # assert one household was deleted
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 2)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 2)
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 2)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 2)

    def test_plot_deletes_household4(self):
        """if you create 3 plots, add members for two and change the plot by subtracting two households, should delete one."""
        #create a plot with 3 households
        plot = PlotFactory(community='test_community', household_count=3, status='occupied')
        # assert household, household structure and an empty log are created
        self.assertEqual(Household.objects.filter(plot=plot).count(), 3)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 3)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 3)
        for index, household_structure in enumerate(HouseholdStructure.objects.filter(household__plot=plot)):
            if not index == 0:
                HouseholdMemberFactory(household_structure=household_structure)
        self.assertEqual(HouseholdMember.objects.filter(household_structure__household__plot=plot).count(), 2)
        # change the number of household to 2
        plot.household_count = 2
        plot.save()
        # assert one household was deleted
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 2)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 2)
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 2)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 2)

    def test_plot_add_households(self):
        """if you add and delete and add back, household identifier should still be unique."""
        plot = PlotFactory(community='test_community', household_count=1, status='occupied')
        print plot.plot_identifier
        plot.household_count = 2
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 3
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 1
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 2
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 3
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 4
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 5
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 6
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 7
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 8
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 9
        self.assertIsNone(plot.save())
        print [hh.household_identifier for hh in Household.objects.filter(plot=plot)]
        plot.household_count = 10
        self.assertRaises(ValidationError, plot.save)

    def test_only_occupied_have_households(self):
        self.assertRaises(ValidationError, PlotFactory, community='test_community', household_count=1, status='non-residential')
        self.assertRaises(ValidationError, PlotFactory, community='test_community', household_count=1, status='vacant')
        self.assertRaises(ValidationError, PlotFactory, community='test_community', household_count=0, status='occupied')

    def test_plot_confirms_plot_and_household(self):
        plot = PlotFactory(community='test_community', household_count=1, status='occupied')
        self.assertEqual(Household.objects.get(plot=plot).action, 'unconfirmed')
        plot.gps_degrees_e = 22
        plot.gps_degrees_s = 22
        plot.gps_minutes_e = 22
        plot.gps_minutes_s = 22
        plot.save()
        self.assertEqual(Plot.objects.get(pk=plot.pk).action, 'confirmed')

    def test_plot_gets_community(self):
        """Plot gets community from settings"""
        current_community = settings.CURRENT_COMMUNITY
        plot = PlotFactory(household_count=1, status='occupied')
        

#     def test_plot_creates_household4(self):
#         """if you change a plot by subtracting a households should try to delete a household without any members or household log."""
#         plot = PlotFactory(community='test_community', household_count=2)
#         self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
#         
#         plot.household_count = 1
#         plot.save()
#         self.assertEqual(Household.objects.filter(plot=plot).count(), 1)

#     def test_identifier(self):
#         print 'create a survey'
#         SurveyFactory()
#         print 'get site mappers'
#         site_mappers.autodiscover()
#         print 'get one mapper'
#         mapper = site_mappers.get(site_mappers.get_as_list()[0])
#         print 'mapper is {0}'.format(mapper().get_map_area())
#         print 'init plot identifier class'
#         plot_identifier = PlotIdentifier(community=mapper().get_map_code())
#         self.assertEqual(PlotIdentifierHistory.objects.all().count(), 0)
#         print 'get the plot_identifier, mode times than the modulus'
#         id1 = plot_identifier.get_identifier()
#         self.assertEqual(PlotIdentifierHistory.objects.all().count(), 1)
#         n = 20
#         for i in range(0, n):
#             plot_identifier.get_identifier()
#         id_last = plot_identifier.get_identifier()
#         self.assertEqual(PlotIdentifierHistory.objects.all().count(), n + 2)
#         print 'length is consistent'
#         self.assertEqual(len(id1), len(id_last))
#         print 'create a plot model instance for community {0}'.format(mapper().get_map_area())
#         plot = PlotFactory(community=mapper().get_map_area())
#         print 'assert plot_identifier is set'
#         self.assertIsNotNone(plot.plot_identifier)
#         print plot.plot_identifier
#         print 'assert expected number of instances in PlotIdentifierHistory ({0})'.format(n + 3)
#         self.assertEqual(PlotIdentifierHistory.objects.all().count(), n + 3)
