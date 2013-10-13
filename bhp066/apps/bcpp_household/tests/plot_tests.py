from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError

from edc.map.classes import site_mappers, Mapper

from apps.bcpp_survey.tests.factories import SurveyFactory

from ..classes  import PlotIdentifier
from ..models import PlotIdentifierHistory, Household, HouseholdLog, HouseholdLogEntry, Plot
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
        """if you create a plot, should create one household."""

        plot = PlotFactory(community='test_community', num_household=1, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)

    def test_plot_creates_household2(self):
        """if you create a plot with two households should create two households."""
        plot = PlotFactory(community='test_community', num_household=2, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_plot_creates_household3(self):
        """if you change a plot by adding a second households should create another household."""
        plot = PlotFactory(community='test_community', num_household=1, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)
        plot.num_household = 2
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_plot_deletes_household1(self):
        """if you change a plot by subtracting a household should delete last created household."""
        plot = PlotFactory(community='test_community', num_household=2, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        plot.num_household = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)

    def test_plot_deletes_household2(self):
        """if you change a plot by subtracting a household should delete last created household."""
        plot = PlotFactory(community='test_community', num_household=2, status='occupied')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        for household_log in HouseholdLog.objects.filter(household_structure__household__plot=plot):
            HouseholdLogEntry.objects.create(household_log=household_log, report_datetime=datetime.today())
        plot.num_household = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_only_occupied_have_households(self):
        self.assertRaises(ValidationError, PlotFactory, community='test_community', num_household=1, status='non-residential')
        self.assertRaises(ValidationError, PlotFactory, community='test_community', num_household=1, status='vacant')
        self.assertRaises(ValidationError, PlotFactory, community='test_community', num_household=0, status='occupied')

    def test_plot_confirms_plot_and_household(self):
        plot = PlotFactory(community='test_community', num_household=1, status='occupied')
        self.assertEqual(Household.objects.get(plot=plot).action, 'unconfirmed')
        plot.gps_degrees_e = 22
        plot.gps_degrees_s = 22
        plot.gps_minutes_e = 22
        plot.gps_minutes_s = 22
        plot.save()
        self.assertEqual(Plot.objects.get(pk=plot.pk).action, 'confirmed')

#     def test_plot_creates_household4(self):
#         """if you change a plot by subtracting a households should try to delete a household without any members or household log."""
#         plot = PlotFactory(community='test_community', num_household=2)
#         self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
#         
#         plot.num_household = 1
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
