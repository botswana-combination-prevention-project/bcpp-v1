from django.test import TestCase

from bhp066.apps.bcpp_household.tests.factories.plot_factory import PlotFactory
from bhp066.apps.bcpp_household.classes.notebook_plot_allocation import NotebookPlotAllocation
from bhp066.apps.bcpp_household.models.plot import Plot
from bhp066.apps.bcpp_household.models.notebook_plot_list import NotebookPlotList

from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.lab.lab_profile.classes import site_lab_profiles

from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp.app_configuration.classes.app_configuration import BcppAppConfiguration
from bhp066.apps.bcpp_subject.visit_schedule.bcpp_subject import BcppSubjectVisitSchedule
from django.test.utils import override_settings


class TestNotebookPlotAllocation(TestCase):

    @override_settings(CURRENT_COMMUNITY='test_community', CURRENT_MAPPER='test_community', SITE_CODE='01')
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

    def test_allocation_even(self):
        Plot.objects.all().delete()
        for _ in range(0, 50):
            PlotFactory(community=self.community)
        plots = Plot.objects.all()
        self.assertEqual(50, plots.count())
        allocation = NotebookPlotAllocation(plots, 5)
        allocation.distributed_notebook_plot_list
        for i in range(0, 5):
            self.assertEqual(len(allocation.machine_notebook_plot_list(i)), 10)

    def test_distribute_remainder(self):
        Plot.objects.all().delete()
        for _ in range(0, 13):
            PlotFactory(community=self.community)
        plots = Plot.objects.all()
        self.assertEqual(13, plots.count())
        allocation = NotebookPlotAllocation(plots, 2)
        allocation.distributed_notebook_plot_list
        for i in range(0, 1):
            self.assertEqual(len(allocation.machine_notebook_plot_list(i)), 7)

    def test_create_notebook_plot(self):
        Plot.objects.all().delete()
        for _ in range(0, 13):
            PlotFactory(community=self.community)
        plots = Plot.objects.all()
        self.assertEqual(13, plots.count())
        allocation = NotebookPlotAllocation(plots, 2)
        allocation.distributed_notebook_plot_list

        allocation.create_notebook_plot_list(0)
        self.assertEqual(NotebookPlotList.objects.all().count(), 7)

    def test_generate_notebook_identifiers(self):
        machines = []
        host = 'bcpp'
        plot_identifier = '10101-0'
        survey = surveys.filter(survey_slug='bcpp-year-2').first()
        for i in range(5):
            NotebookPlotList.create(
                plot_identifier=plot_identifier + str(i), community='test_community',
                notebook=host + str(i), survey=survey)
        for i in range(5):
            PlotFactory(plot_identifier=plot_identifier + str(i))
            
        for j in range(5):
            self.assertEqual(Plot.objects.filter(plot_identifier=))
