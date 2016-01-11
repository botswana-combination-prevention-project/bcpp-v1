from django.test import TestCase
from django.core.exceptions import ValidationError

from edc.map.classes import site_mappers

from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.map.classes import site_mappers

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule

from bhp066.apps.bcpp_survey.models import Survey

from ..models import (HouseholdIdentifierHistory, Household, HouseholdStructure, Plot, HouseholdLog,
                      PlotIdentifierHistory)

from .factories.plot_factory import PlotFactory
from .factories.household_log_entry_factory import HouseholdLogEntryFactory


class TestHouseholds(TestCase):
    """Test plots and Households."""

<<<<<<< HEAD
>>>>>>> 3890b2539f5e770330f2b642fdf6cb254e3a2865
    def setUp(self):
        site_mappers.autodiscover()
        self.mapper = site_mappers.get(site_mappers.get_as_list()[0])

    def test_identifier(self):
        """Assert plot creates an identifier"""
        SurveyFactory()
        plot = PlotFactory(community=self.mapper().get_map_area())
<<<<<<< HEAD
=======
=======

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.community = 'test_community'
        self.mapper = site_mappers.get_registry(self.community)()

        self.survey = Survey.objects.all()[0]

    def test_identifier(self):
        """Assert plot creates an identifier"""
        plot = PlotFactory(community=self.community)
>>>>>>> master
>>>>>>> 3890b2539f5e770330f2b642fdf6cb254e3a2865
        self.assertIsNotNone(plot.plot_identifier)

    def test_identifier_code(self):
        """Assert plot creates an identifier prefixed with the community code"""
        plot = PlotFactory(community=self.community)
        self.assertEquals(self.mapper.map_code, plot.plot_identifier[:2])

    def test_plot_creates_household1(self):
        """Assert plot creates one household if residential habitable"""
        PlotFactory(community=self.community, household_count=1,
                    status='residential_habitable')
        self.assertEqual(Household.objects.all().count(), 1)

    def test_plot_creates_household2(self):
        """Assert plot creates two households if residential habitable"""
        PlotFactory(community=self.community, household_count=2,
                    status='residential_habitable')
        self.assertEqual(Household.objects.all().count(), 2)

    def test_plot_creates_household3(self):
        """Assert plot creates 2 households if residential habitable and three surveys"""
        PlotFactory(community=self.community, household_count=2,
                    status='residential_habitable')
        self.assertEqual(Household.objects.all().count(), 2)

    def test_plot_creates_household4(self):
        """Assert plot creates two additional households if household_count increased to 3"""
        plot = PlotFactory(community=self.community, household_count=1,
                           status='residential_habitable')
        plot.household_count = 3
        plot.save()
        self.assertEqual(Household.objects.all().count(), 3)

    def test_plot_creates_household5(self):
        """Assert plot creates deletes two households if household_count increased to 5 then decreased to 3."""
        plot = PlotFactory(community=self.community, household_count=1,
                           status='residential_habitable')
        plot.household_count = 5
        plot.save()
        self.assertEqual(Household.objects.all().count(), 5)
        plot.household_count = 3
        plot.save()
        self.assertEqual(Household.objects.all().count(), 3)

    def test_cannot_delete_household_with_logentry(self):
        """Assert household cannot be deleted if has a household log entry."""

        plot = PlotFactory(community=self.community, household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            household_structure = HouseholdStructure.objects.filter(survey=self.survey, household=household)
            household_log = HouseholdLog.objects.get(household_structure=household_structure)
            HouseholdLogEntryFactory(household_log=household_log)
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.all().count(), 3)
        plot = Plot.objects.get(plot_identifier=plot.plot_identifier)
        self.assertEquals(plot.household_count, 3)

    def test_cannot_delete_household_with_eligible_members(self):
        """Assert cannot_delete_household_with_eligible_members"""

        plot = PlotFactory(community=self.community, household_count=3,
                           status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            household_structure = HouseholdStructure.objects.filter(survey=self.survey, household=household)
            household_log = HouseholdLog.objects.get(household_structure=household_structure)
            household_log_entry = HouseholdLogEntryFactory(household_log=household_log)
        household_log_entry.delete()
        plot.household_count = 1
        plot.save()
        self.assertEqual(Household.objects.all().count(), 2)
        plot = Plot.objects.get(plot_identifier=plot.plot_identifier)
        self.assertEquals(plot.household_count, 2)

    def test_household_count1(self):
        """Asserts household count is 1 after 1 household is created."""

        plot = PlotFactory(community=self.community, household_count=1,
                           status='residential_habitable')
        plot = Plot.objects.get(plot_identifier=plot.plot_identifier)
        self.assertEquals(plot.household_count, 1)

    def test_household_count2(self):
        """Asserts household count is 3 after 2 households are added after create."""

        plot = PlotFactory(community=self.community, household_count=1,
                           status='residential_habitable')
        plot = Plot.objects.get(plot_identifier=plot.plot_identifier)
        plot.household_count = 3
        plot.save()
        self.assertEquals(plot.household_count, 3)

    def test_household_count3(self):
        """Asserts household count is 3 after 4 households are added after create and then 2 removed."""

        plot = PlotFactory(community=self.community, household_count=1,
                           status='residential_habitable')
        plot = Plot.objects.get(plot_identifier=plot.plot_identifier)
        plot.household_count = 5
        plot.save()
        plot.household_count = 3
        self.assertEquals(plot.household_count, 3)

    def test_plot_creates_household_structure(self):
        """Assert plot creates 6 household_structures if residential habitable and three surveys (3 for each household)."""

        PlotFactory(community=self.community, household_count=2,
                    status='residential_habitable')
        self.assertEqual(HouseholdStructure.objects.all().count(), 6)

    def test_plot_creates_households_with_identifiers(self):
        """Assert plot creates two households with identifier"""

        PlotFactory(community=self.community, household_count=2,
                    status='residential_habitable')
        for household in Household.objects.all():
            self.assertIsNotNone(household.household_identifier)

    def test_plot_creates_households_with_identifiers2(self):
        """Assert plot creates two households with identifier"""

        PlotFactory(community=self.community, household_count=2,
                    status='residential_habitable')
        for household in Household.objects.all():
            self.assertIsNotNone(household.household_identifier)

    def test_plot_creates_households_with_unique_identifiers(self):
        """Assert plot creates unique household identifiers"""

        household_identifier = []
        PlotFactory(community=self.community, household_count=8,
                    status='residential_habitable')
        for household in Household.objects.all():
            household_identifier.append(household.household_identifier)
        PlotFactory(community=self.community, household_count=8,
                    status='residential_habitable')
        for household in Household.objects.all():
            household_identifier.append(household.household_identifier)
        PlotFactory(community=self.community, household_count=8,
                    status='residential_habitable')
        for household in Household.objects.all():
            household_identifier.append(household.household_identifier)
        PlotFactory(community=self.community, household_count=8,
                    status='residential_habitable')
        for household in Household.objects.all():
            household_identifier.append(household.household_identifier)
        PlotFactory(community=self.community, household_count=8,
                    status='residential_habitable')
        for household in Household.objects.all():
            household_identifier.append(household.household_identifier)
        self.assertEqual(household_identifier.sort(), list(set(household_identifier)).sort())

    def test_household_derives_identifier_from_plot(self):
        """Assert household_identifier is derived from plot"""
        plot = PlotFactory(community=self.community, household_count=8,
                           status='residential_habitable')
        for household in Household.objects.all():
            self.assertEqual(household.household_identifier.split('-')[0][:6], '{0}'.format(plot.plot_identifier.split('-')[0]))

    def test_plot_identifier_history_updated(self):

        plot = PlotFactory(community=self.community, household_count=8,
                           status='residential_habitable')
        for plot in Plot.objects.all():
            self.assertEquals(PlotIdentifierHistory.objects.filter(
                identifier=plot.plot_identifier).count(), 1)

    def test_household_identifier_history_updated(self):
 
        plot = PlotFactory(community=self.community, household_count=8, status='residential_habitable')
        for household in Household.objects.filter(plot=plot):
            # print household.household_identifier, household.plot.plot_identifier
            self.assertEquals(HouseholdIdentifierHistory.objects.filter(
                plot_identifier=household.plot.plot_identifier,
                identifier=household.household_identifier).count(), 1)

    def test_create_household5(self):
        """Assert household.plot is not None when household is created."""

        PlotFactory(community=self.community, household_count=8,
                    status='residential_habitable')
        for household in Household.objects.all():
            self.assertIsNotNone(household.plot)

    def test_max_households(self):

        plot = PlotFactory(community=self.community, household_count=8,
                           status='residential_habitable')
        plot.household_count = 10
        self.assertRaises(ValidationError, plot.save)
