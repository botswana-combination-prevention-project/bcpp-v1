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
    map_area = 'gumare'
    map_code = '35'
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

    def test_plot_deletes_household(self):
        """if you change a plot by subtracting a household should delete last created household."""
        plot = PlotFactory(community='gumare', household_count=2, status='residential_habitable')
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 1)

    def test_household_structures(self):
        """ Test whether the number of household_structures are correct after deleting other household(s). """
        plot = PlotFactory(community='gumare', household_count=2, status='residential_habitable')
        plot.household_count = 1
        plot.save()
        self.assertEqual(HouseholdStructure.objects.filter(household__plot=plot).count(), 3)

    def test_plot_logs(self):
        """ Test whether the number of plot_logs are correct after deleting other household(s). """
        plot = PlotFactory(community='gumare', household_count=2, status='residential_habitable')
        plot.household_count = 1
        plot.save()
        self.assertEqual(HouseholdLog.objects.filter(household_structure__household__plot=plot).count(), 3)

    def test_plot_update(self):
        """ Updating a plot without changing households number should not change the delete or add new households. """
        plot = PlotFactory(community='gumare', household_count=2, status='residential_habitable')
        plot.household_count = 2
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_plot_update_with_zero(self):
        """ Updating a plot without changing households number should not change the delete or add new households. """
        plot = PlotFactory(community='gumare', household_count=2, status='residential_habitable')
        plot.household_count = 0
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_household_add(self):
        """ Updating a plot without changing households number should not change the delete or add new households. """
        plot = PlotFactory(community='gumare', household_count=1, status='residential_habitable')
        plot.household_count = 2
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_plot_deletes_household_with_data(self):
        """For all households with data cannot be deleted. Test whether the delete will failed. """
        plot = PlotFactory(community='gumare', household_count=2, status='residential_habitable')
        plot.household_count = 2
        plot.save()
        for hh in Household.objects.filter(plot=plot):
            hs = HouseholdStructure.objects.filter(household=hh).first()
            hl = HouseholdLog.objects.filter(household_structure=hs).first()
            HouseholdLogEntry.objects.create(household_log=hl, report_datetime=datetime.today())
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.filter(plot=plot).count(), 2)

    def test_plot_status_change(self):
        """ Test that if the status of the plot changes and the household count is zero a household is deleted. """
        plot = PlotFactory(community='gumare', household_count=1, status='residential_habitable')
        self.assertEqual(plot.status, 'residential_habitable')
#         plot.household_count = 0
        plot.status = 'residential_not_habitable'
        plot.save()
        self.assertEqual(plot.status, 'residential_not_habitable')
        self.assertEqual(Household.objects.filter(plot=plot).count(), 0)
