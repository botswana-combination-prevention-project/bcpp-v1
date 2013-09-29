from django.test import TestCase
from edc_core.bhp_map.classes import site_mappers
from bcpp_survey.tests.factories import SurveyFactory
from ..classes  import PlotIdentifier
from ..models import PlotIdentifierHistory
from .factories import PlotFactory


class PlotTests(TestCase):

    def test_identifier(self):
        print 'create a survey'
        SurveyFactory()
        print 'get site mappers'
        site_mappers.autodiscover()
        print 'get one mapper'
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        print 'mapper is {0}'.format(mapper().get_map_area())
        print 'init plot identifier class'
        plot_identifier = PlotIdentifier(community=mapper().get_map_code())
        self.assertEqual(PlotIdentifierHistory.objects.all().count(), 0)
        print 'get the plot_identifier, mode times than the modulus'
        id1 = plot_identifier.get_identifier()
        self.assertEqual(PlotIdentifierHistory.objects.all().count(), 1)
        n = 20
        for i in range(0, n):
            plot_identifier.get_identifier()
        id_last = plot_identifier.get_identifier()
        self.assertEqual(PlotIdentifierHistory.objects.all().count(), n + 2)
        print 'length is consistent'
        self.assertEqual(len(id1), len(id_last))
        print 'create a plot model instance for community {0}'.format(mapper().get_map_area())
        plot = PlotFactory(community=mapper().get_map_area())
        print 'assert plot_identifier is set'
        self.assertIsNotNone(plot.plot_identifier)
        print plot.plot_identifier
        print 'assert expected number of instances in PlotIdentifierHistory ({0})'.format(n + 3)
        self.assertEqual(PlotIdentifierHistory.objects.all().count(), n + 3)
