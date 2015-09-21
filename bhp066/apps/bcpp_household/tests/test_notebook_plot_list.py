from django.test import TestCase

from bhp066.apps.bcpp_household.tests.factories.plot_factory import PlotFactory
from bhp066.apps.bcpp_household.classes.notebook_plot_allocation import NotebookPlotAllocation
from bhp066.apps.bcpp_household.models.plot import Plot
from bhp066.apps.bcpp_household.models.notebook_plot_list import NotebookPlotList

from edc.map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.lab.lab_profile.classes import site_lab_profiles

from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp.app_configuration.classes.app_configuration import BcppAppConfiguration
from bhp066.apps.bcpp_subject.visit_schedule.bcpp_subject import BcppSubjectVisitSchedule


class TestNotebookPlotAllocation(TestCase):

    community = 'otse'

    def setUp(self):
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
