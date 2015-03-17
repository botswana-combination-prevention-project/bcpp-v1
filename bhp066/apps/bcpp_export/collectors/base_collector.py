from datetime import datetime

from edc.export.helpers import ExportObjectHelper
from edc.map.classes import site_mappers

from ..plans import export_plan as default_export_plan


class BaseCollector(object):

    def __init__(self, export_plan=None, community=None, exception_cls=None):
        self.delimiter = "|"
        self.for_csv = False
        self.filename = None
        self.test_run = False
        self.write_header = True
        self.export_plan = export_plan or default_export_plan
        self.export_plan.notification_plan = 'rdb'
        self.exception_cls = exception_cls or TypeError
        site_mappers.autodiscover()
        try:
            del site_mappers._registry['bhp']
        except KeyError:
            pass
        try:
            del site_mappers._registry['test_community']
        except KeyError:
            pass
        if community:
            self.community_list = [community]
        else:
            self.mappers = site_mappers.sort_by_pair()
            self.community_list = [mapper().community for mapper in self.mappers.itervalues()]

    def __repr__(self):
        return '{0}({1.export_plan!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.export_plan!r}'.format(self)

    def export_to_csv(self):
        """Prepares and passes helper instances one by one to method _export.

        Must be overridden.

        for example::
            for community in self.community_list:
                for plot_model in PlotModel.objects.filter(community=community).order_by('plot_identifier'):
                    plot = Plot(plot=plot_model)
                    self._export(plot)
                    if self.test_run:
                        break
        """
        raise TypeError('Method must be overridden.')

    def _export(self, instance):
        """Calls the csv writer to append each instance to the current file."""
        instance.customize_for_csv()
        self.export_plan = self.delimiter
        if not self.export_plan.fields:
            self.export_plan.fields = instance.data.keys()
        if not self.filename:
            self.filename = '{0}_{1}.csv'.format(
                instance.__class__.__name__, datetime.today().strftime('%Y%m%d%H%M%S'))
        export_model_helper = ExportObjectHelper(
            self.export_plan, filename=self.filename, exception_cls=self.exception_cls)
        export_model_helper.writer.write_to_file([instance], self.write_header)
        self.write_header = False  # only write header once
