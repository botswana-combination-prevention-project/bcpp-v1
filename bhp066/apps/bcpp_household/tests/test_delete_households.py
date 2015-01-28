from datetime import datetime
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.map.classes import site_mappers, Mapper
 
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule

from .factories import PlotFactory
from ..models import Household, HouseholdStructure, HouseholdLog, HouseholdLogEntry, Plot

 
class TestPlotMapper(Mapper):
    map_area = 'mmankgodi'
    map_code = '19'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.011111
    gps_center_lon = 25.741111
    radius = 5.5
    location_boundary = ()
 
# site_mappers.register(TestPlotMapper)
 
 
class DeleteHouseholdTests(TestCase):
 
    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
 
    def test_plot_deletes_household1(self):
        """if you change a plot by subtracting a household should delete last created household."""
        plot = PlotFactory(community='mmankgodi', household_count=2, status='residential_habitable')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        plot.household_count = 1
        plot.save()
        "Saved going to assert"
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)
 
    def test_plot_deletes_household2(self):
        """if you change a plot by subtracting a household should delete last created household."""
        plot = PlotFactory(community='mmankgodi', household_count=2, status='residential_habitable')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 6)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 6)
        for household_log in HouseholdLog.objects.filter(household_structure__household__plot=plot):
            HouseholdLogEntry.objects.create(household_log=household_log, report_datetime=datetime.today())
        plot.household_count = 2
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 6)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 6)
 
    def test_plot_deletes_household3(self):
        """if you create 3 plots, add log entries for two and change the plot by subtracting two households, should delete one."""
        #create a plot with 3 households
        plot = PlotFactory(community='mmankgodi', household_count=3, status='residential_habitable')
        # assert household, household structure and an empty log are created
        self.assertEqual(Household.objects.filter(plot=plot).count(), 3)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 9)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 9)
        # create a log entry for two households
        for index1, household in enumerate(Household.objects.filter(plot=plot)):
            if not index1 == 2:
                for index, household_log in enumerate(HouseholdLog.objects.filter(household_structure__household=household)):
               # if not index == 0:
                    print 'CREATING ENTRY FOR**'+household_log.household_structure.household.household_identifier
                    HouseholdLogEntry.objects.create(household_log=household_log, report_datetime=datetime.today())
        self.assertEqual(HouseholdLogEntry.objects.filter(household_log__household_structure__household__plot=plot).count(), 6)
        # change the number of household to 2
        plot.household_count = 2
        plot.save()
        # assert one household was deleted
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 6)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 6)
        #Only 1 household could be deleted instead of the proposed 2, make sure that plot.household_count is
        #updated to the correct value.
        self.assertEqual(plot.household_count, 2)
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 2)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 2)
 
    def test_plot_deletes_household4(self):
        """if you create 3 plots, add members for two and change the plot by subtracting two households, should delete one."""
        #create a plot with 3 households
        plot = PlotFactory(community='mmankgodi', household_count=3, status='residential_habitable')
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
        #Only 1 household could be deleted instead of the proposed 2, make sure that plot.household_count is
        #updated to the correct value.
        self.assertEqual(plot.household_count, 2)
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 2)
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 2)
