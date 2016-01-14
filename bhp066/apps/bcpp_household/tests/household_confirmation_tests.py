# import datetime
#
# from django.test import TestCase
#
# from edc.map.classes import site_mappers
#
# from bhp066.apps.bcpp_household.models import Household
# from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory
#
# from .factories import PlotFactory
#
#
# class HouseholdConfirmTests(TestCase):
#
#     def test_household_confirmation_by_plot(self):
#
#         print "*********************************"
#         print 'create a survey'
#         SurveyFactory()
#         SurveyFactory()
#         print 'get site mappers'
#         site_mappers.autodiscover()
#         print 'get one mapper'
#         mapper = site_mappers.get(site_mappers.get_as_list()[0])
#         print 'mapper is {0}'.format(mapper().get_map_area())
#         print 'create a plot model instance for community {0}'.format(mapper().get_map_area())
#         self.assertEqual(Household.objects.all().count(), 0)
#         plot = PlotFactory(availability_datetime=datetime.datetime(2013, 10, 8, 10, 47, 33), status='occupied', gps_degrees_s=24, gps_minutes_s=39.248, gps_degrees_e=25, gps_minutes_e=54.534)
#         print 'assert plot_identifier is set'
#         self.assertIsNotNone(plot.plot_identifier)
#         print plot.plot_identifier
#         print "assert created a Household"
#         self.assertEqual(Household.objects.all().count(), 1)
#         print "check if household action is changed to composition"
#         self.assertEqual(Household.objects.filter(plot__plot_identifier=plot.plot_identifier)[0].action, 'confirmed')
#         print "Household action is :", Household.objects.filter(plot__plot_identifier=plot.plot_identifier)[0].action
#         print "*****************************************"
