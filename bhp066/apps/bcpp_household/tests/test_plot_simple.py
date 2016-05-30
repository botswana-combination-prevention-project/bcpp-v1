from datetime import date
# from dateutil.relativedelta import relativedelta

from django.db.models import Model
from django.test import TestCase
from django.test.utils import override_settings

# from edc_map.classes import site_mappers

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups


from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp.app_configuration.classes.app_configuration import BcppAppConfiguration
from bhp066.apps.bcpp_household.classes import PlotIdentifier
from bhp066.apps.bcpp_household.models import Household
from bhp066.apps.bcpp_household.models import Plot
from bhp066.apps.bcpp_household.models import PlotIdentifierHistory
# from bhp066.apps.bcpp_household.utils.survey_dates_tuple import SurveyDatesTuple
from bhp066.config.databases import TESTING_SQLITE


class TestPlotSimple(TestCase):

    @override_settings(LIMIT_EDIT_TO_CURRENT_SURVEY=True, LIMIT_EDIT_TO_CURRENT_COMMUNITY=True, FILTERED_DEFAULT_SEARCH=True)
    def setUp(self):
        self.community = 'test_community'
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
#         mapper_cls = site_mappers._registry['test_community']
#         mapper_cls.survey_dates = {
#             'bcpp-year-1': SurveyDatesTuple(
#                 name='bhs',
#                 start_date=date.today() - relativedelta(days=10),
#                 full_enrollment_date=date.today() + relativedelta(days=100),
#                 end_date=date.today() + relativedelta(days=110),
#                 smc_start_date=date.today() + relativedelta(days=100)),
#             'bcpp-year-2': SurveyDatesTuple(
#                 name='t1',
#                 start_date=date.today() - relativedelta(days=10) + relativedelta(years=1),
#                 full_enrollment_date=date.today() + relativedelta(days=100) + relativedelta(years=1),
#                 end_date=date.today() + relativedelta(days=110) + relativedelta(years=1),
#                 smc_start_date=date.today() + relativedelta(days=100) + relativedelta(years=1))}
#         site_mappers._registry['test_community'] = mapper_cls

    def test_simple_create(self):

        original_save = Plot.save
        Plot.save = Model.save

        plot = Plot.objects.create()
        self.assertEqual(plot.created.date(), date.today())
        self.assertEqual(plot.modified.date(), date.today())
        self.assertEqual(plot.user_created, '')
        self.assertEqual(plot.user_modified, '')
        self.assertNotEqual(plot.revision, '')
        self.assertIsNotNone(plot.revision)
        self.assertNotEqual(plot.hostname_created, '')
        self.assertIsNotNone(plot.hostname_created)
        Plot.save = original_save

    def test_plot_identifier_class(self):
        plot_identifier = PlotIdentifier('10', 'default').get_identifier()
        self.assertEqual(plot_identifier, '100001-00')
        self.assertEqual(PlotIdentifierHistory.objects.all().count(), 1)
        plot_identifier_history = PlotIdentifierHistory.objects.get(identifier='100001-00')
        self.assertEqual(plot_identifier_history.created.date(), date.today())
        self.assertEqual(plot_identifier_history.modified.date(), date.today())

    def test_create_household_given_plot_identifier(self):
        original_save = Plot.save
        Plot.save = Model.save
        plot_identifier = PlotIdentifier('10', 'default').get_identifier()
        plot = Plot.objects.create(plot_identifier=plot_identifier)
        Household.objects.create(plot=plot)
        Plot.save = original_save

    def test_create_plot_and_households(self):
        plot = Plot.objects.create(household_count=1, community='test_community')
        self.assertEqual(plot.plot_identifier, '010001-02')
        self.assertEqual(Household.objects.count(), 1)
        plot = Plot.objects.create(household_count=5, community='test_community')
        self.assertEqual(plot.plot_identifier, '010002-03')
        self.assertEqual(Household.objects.count(), 6)

LoginTestCase = override_settings(
    DATABASE={'default': TESTING_SQLITE['default']},
    DEVICE_ID=99,
    SITE_CODE='01',
    CURRENT_COMMUNITY='test_community',
    CURRENT_SURVEY='bcpp-year-1',
    VERIFY_GPS=False,
    VERIFY_GPS_LOCATION=False,
    VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER=False,
    LIMIT_EDIT_TO_CURRENT_SURVEY=False,
    LIMIT_EDIT_TO_CURRENT_COMMUNITY=False,
    FILTERED_DEFAULT_SEARCH=False)(TestPlotSimple)
