from datetime import datetime
 
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
 
from edc.map.exceptions import MapperError

from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from ..choices import (PLOT_STATUS, SELECTED, INACCESSIBLE, ACCESSIBLE)
from ..constants import CONFIRMED, UNCONFIRMED
from ..models import Household, HouseholdStructure, Plot

from .factories import PlotFactory, PlotLogEntryFactory, PlotLogFactory

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule


# class TestPlotMapper(Mapper):
#     map_area = 'test_community'
#     map_code = '999'
#     regions = []
#     sections = []
#     landmarks = []
#     gps_center_lat = -25.011111
#     gps_center_lon = 25.741111
#     radius = 5.5
#     location_boundary = ()
#
# site_mappers.register(TestPlotMapper)


class PlotTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        SurveyFactory()
 
    def test_plot_creates_household1(self):
        """if you create a plot as residential_habitable, should create one household."""

        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)

    def test_plot_creates_household2(self):
        """if you create a plot with two households should create two households."""
        plot = PlotFactory(community='test_community', household_count=2, status='residential_habitable')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_plot_creates_household3(self):
        """if you change a plot by adding a second households should create another household."""
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)
        plot.household_count = 2
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
 
    def test_plot_creates_household4(self):
        """if you create a plot as None, should create one household."""
        plot = PlotFactory(community='test_community', household_count=0, status=None)
        self.assertEqual(Household.objects.filter(plot=plot).count(), 0)
 
    def test_plot_add_households(self):
        """if you add and delete and add back, household identifier should still be unique."""
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
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
 
    def test_only_residential_habitable_have_households(self):
        self.assertRaises(ValidationError, PlotFactory, community='test_community', household_count=1, status='non-residential')
        self.assertRaises(ValidationError, PlotFactory, community='test_community', household_count=1, status='residential_not_habitable')
        self.assertRaises(ValidationError, PlotFactory, community='test_community', household_count=0, status='residential_habitable')
 
    def test_plot_confirms_plot_and_household(self):
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable', gps_target_lat=-25.011111, gps_target_lon=25.741111)
        self.assertEqual(Household.objects.get(plot=plot).action, 'unconfirmed')
        plot.gps_degrees_e = 25
        plot.gps_degrees_s = 25
        plot.gps_minutes_s = .011111 * 60
        plot.gps_minutes_e = .741111 * 60
        plot.save()
        self.assertEqual(Plot.objects.get(pk=plot.pk).action, 'confirmed')
 
    def test_plot_verifies_gps1(self):
        """accepts gps within community boundary."""
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
        self.assertEqual(Household.objects.get(plot=plot).action, 'unconfirmed')
        plot.gps_degrees_e = 25
        plot.gps_degrees_s = 25
        plot.gps_minutes_s = .01000 * 60
        plot.gps_minutes_e = .74000 * 60
        self.assertIsNone(plot.save())
 
    def test_plot_verifies_gps2(self):
        """rejects gps not within community boundary."""
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
        self.assertEqual(Household.objects.get(plot=plot).action, 'unconfirmed')
        plot.gps_degrees_e = 25
        plot.gps_degrees_s = 25
        plot.gps_minutes_e = 22
        plot.gps_minutes_s = 22
        self.assertRaisesRegexp(MapperError, 'does not fall within this community', plot.save)
 
    def test_plot_form_verifies_gps1(self):
        """plot_form catches error if gps not within community boundary."""
        from ..forms import PlotForm
        plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
        plot.gps_degrees_e = 25
        plot.gps_degrees_s = 25
        plot.gps_minutes_e = .22
        plot.gps_minutes_s = .22
        plot_form = PlotForm()
        plot_form.instance = plot
        plot_form.cleaned_data = {}
        self.assertRaisesRegexp(forms.ValidationError, 'does not fall within this community', plot_form.clean)
 
    def test_plot_gets_community1(self):
        """Plot DOES NOT get community from settings if None"""
        self.assertRaisesRegexp(ValidationError, 'Attribute \'community\' may not be None for model', PlotFactory, household_count=1, status='residential_habitable')
 
    def test_plot_community1(self):
        """Plot does not save if community is None"""
        self.assertRaisesRegexp(ValidationError, 'Attribute \'community\' may not be None for model', PlotFactory, household_count=1, status='residential_habitable', community=None)
 
    def test_plot_community2(self):
        """Plot does not save if community is not valid community from mapper classes."""
        self.assertRaisesRegexp(MapperError, 'invalid_community_name is not a valid mapper ', PlotFactory, household_count=1, status='residential_habitable', community='invalid_community_name')
 
    def test_plot_save_on_change(self):
        """Allows change of residential_habitable plot even though no log entry or members have been added yet."""
        plot = PlotFactory(status=None, community='test_community')
        plot.status = 'residential_habitable'
        plot.household_count = 1
        self.assertIsNone(plot.save())
        self.assertIsNone(plot.save())
 
    def test_plot_save_on_change2(self):
        """Allows change of residential_habitable plot even though no log entry or members have been added yet."""
        plot = PlotFactory(status=None, community='test_community')
        plot.status = 'residential_habitable'
        plot.household_count = 1
        self.assertIsNone(plot.save())
        household = Household.objects.get(plot=plot)
        HouseholdStructure.objects.filter(household=household).delete()
        household.delete()
        self.assertIsNone(plot.save())
 
    def test_plot_visit_attempts(self):
        from ..models import PlotLog
        plot = PlotFactory(status=None, community='test_community')
        plot_log = plot.plot_log
        self.assertEqual(1,PlotLog.objects.all().count())
        plot_log_entry_1 = PlotLogEntryFactory(plot_log)
        plot_log_entry_2 = PlotLogEntryFactory(plot_log)
        self.assertEqual(2, PlotLog.objects.all().count())
        plot_log_entry_3 = PlotLogEntryFactory(plot_log)
        self.assertRaises(TypeError, PlotLogEntryFactory(plot_log))

    def test_validate_confirm_plot_inaccessible(self):

        plot = PlotFactory(status=None, community='test_community', household_count=0, gps_target_lon=None, gps_target_lat=None)
        plot_log = PlotLogFactory(plot=plot)
        plot_entry = PlotLogEntryFactory(log_status=INACCESSIBLE)
        plot_entry.plot_log = plot_log
        plot_entry.save()
        self.assertEqual(plot.action, UNCONFIRMED)

    def test_validate_confirm_plot_inaccessible2(self):

        plot = PlotFactory(status=None, community='test_community', household_count=0, gps_target_lon=None, gps_target_lat=None)
        plot_log = PlotLogFactory(plot=plot)
        plot_entry = PlotLogEntryFactory(log_status=INACCESSIBLE)
        plot_entry.plot_log = plot_log
        plot_entry.save()
        #
        self.assertFalse(plot.validate_plot_accessible)

    def test_validate_confirm_plot_accessible(self):
        plot = PlotFactory(status=None, community='test_community', household_count=0, gps_target_lon=None, gps_target_lat=None)
        plot_log = PlotLogFactory(plot=plot)
        plot_entry = PlotLogEntryFactory(log_status=ACCESSIBLE)
        plot_entry.plot_log = plot_log
        plot.household_count = 2
        plot.gps_lon = '2.1231'
        plot.gps_lat = '2.123451'
        plot.save()
        self.assertEqual(plot.action, CONFIRMED)

#     def test_identifier(self):plot_log
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
