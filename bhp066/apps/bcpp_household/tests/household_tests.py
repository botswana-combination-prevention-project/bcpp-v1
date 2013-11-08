from django.test import TestCase

from edc.core.identifier.exceptions import IdentifierError
from edc.map.classes import site_mappers

from apps.bcpp_survey.tests.factories import SurveyFactory

from ..classes  import HouseholdIdentifier
from ..models import HouseholdIdentifierHistory, Household, HouseholdStructure

from .factories import PlotFactory, HouseholdFactory


class HouseholdTests(TestCase):

    def test_identifier(self):

        print 'create a survey'
        SurveyFactory()
        SurveyFactory()
        print 'get site mappers'
        site_mappers.autodiscover()
        print 'get one mapper'
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        print 'mapper is {0}'.format(mapper().get_map_area())
        print 'create a plot model instance for community {0}'.format(mapper().get_map_area())
        self.assertEqual(Household.objects.all().count(), 0)
        plot = PlotFactory(community=mapper().get_map_area())
        print 'assert plot_identifier is set'
        self.assertIsNotNone(plot.plot_identifier)
        print plot.plot_identifier
        print "assert created a Household"
        self.assertEqual(Household.objects.all().count(), 1)
        print 'create a household identifier'
        household_identifier = HouseholdIdentifier(plot_identifier=plot.plot_identifier, household_sequence=plot.get_next_household_sequence())
        household_identifier = household_identifier.get_identifier()
        print 'assert household identifier is correctly derived from plot identifier'
        self.assertEqual(household_identifier.split('-')[0], '{0}{1}'.format(plot.plot_identifier.split('-')[0], plot.get_next_household_sequence()))
        print 'household_identifier={0}'.format(household_identifier)
        print 'confirm tracked in household identifier history'
        self.assertEqual(HouseholdIdentifierHistory.objects.all().count(), 2)
        print 'clear history to start over'
        HouseholdIdentifierHistory.objects.all().delete()
        print 'confirm just one households exists(created by plot factory) '
        self.assertEqual(Household.objects.all().count(), 1)
        print 'create a household'
        h1 = HouseholdFactory(plot=plot)
        self.assertEqual(Household.objects.all().count(), 2)
        print h1
        h2 = HouseholdFactory(plot=plot)
        self.assertEqual(Household.objects.all().count(), 3)
        print h2
        h3 = HouseholdFactory(plot=plot)
        self.assertEqual(Household.objects.all().count(), 4)
        print h3
        h4 = HouseholdFactory(plot=plot)
        self.assertEqual(Household.objects.all().count(), 5)
        print h4
        h5 = HouseholdFactory(plot=plot)
        self.assertEqual(Household.objects.all().count(), 6)
        print h5
        h6 = HouseholdFactory(plot=plot)
        self.assertEqual(Household.objects.all().count(), 7)
        print h6
        h7 = HouseholdFactory(plot=plot)
        self.assertEqual(Household.objects.all().count(), 8)
        print h7
        h9 = HouseholdFactory(plot=plot)
        print h9
        print 'assert that you cannot create a tenth household in the same plot'
        self.assertRaises(IdentifierError, HouseholdFactory, plot=plot)
        print 'assert all 9 have 1 householdstructure/survey (2 surveys)'
        self.assertEqual(HouseholdStructure.objects.all().count(), 18)
        print 'try resaving all households'
        for h in Household.objects.all():
            h.save()
        print 'try resaving all householdstructures'
        for hs in HouseholdStructure.objects.all():
            hs.save()
