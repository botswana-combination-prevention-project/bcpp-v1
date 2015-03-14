from apps.bcpp_household.models import Plot as PlotModel

from ..classes import Plot

from .base_collector import BaseCollector


class Plots(BaseCollector):

    """Exports helper.plot instances to CSV.

    For example::
        from apps.bcpp_export.collectors import Plots

        plots = Plots()
        plots.export_to_csv()
    """

    def __init__(self, export_plan=None, community=None, exception_cls=None, include_clinic_plots=False):
        self.include_clinic_plots = include_clinic_plots
        super(Plots, self).__init__(export_plan=export_plan, community=community, exception_cls=exception_cls)

    def export_to_csv(self):
        for community in self.community_list:
            print '{} **************************************'.format(community)
            for plot_model in PlotModel.objects.filter(community=community).order_by('plot_identifier'):
                plot = Plot(plot=plot_model)
                if not plot.plot_identifier.endswith('CLIN-IC') or self.include_clinic_plots:
                    self._export(plot)
                if self.test_run:
                    break
