import sys

from datetime import datetime

from edc.export.classes import ExportDictAsCsv
from edc.export.helpers import ExportObjectHelper
from edc.map.classes import site_mappers

from ..plans import export_plan as default_export_plan


class BaseCollector(object):

    def __init__(self, export_plan=None, community=None, exception_cls=None, delimiter=None):
        self.delimiter = delimiter or "|"
        self.for_csv = False
        self.filename = None
        self.test_run = False
        self.write_header = True
        self.export_plan = export_plan or default_export_plan
        self.export_plan.notification_plan = 'rdb'
        self.exception_cls = exception_cls or TypeError
        self.instances = []
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

    def export(self, instance, filename_prefix=None):
        """Calls the csv writer to append each instance to the current file."""
        instance.customize_for_csv()
        if not self.filename:
            self.filename = '{0}{1}_{2}.csv'.format(
                filename_prefix or '', instance.__class__.__name__, datetime.today().strftime('%Y%m%d%H%M%S'))
        if self.write_header:
            self.output_to_console('Writing to {}\n'.format(self.filename))
        export_model_helper = ExportObjectHelper(
            self.export_plan,
            delimiter=self.delimiter,
            fields=instance.data.keys(),
            filename=self.filename,
            exception_cls=self.exception_cls)
        export_model_helper.writer_cls = ExportDictAsCsv
        export_model_helper.writer.write_to_file([instance.data], self.write_header)
        self.write_header = False  # only write header once

    def collect(self, instance):
        self.instances.append(instance)

    def export_all(self):
        """Calls the csv writer to append each instance to a list then write all to file at once."""
        instances_for_csv = (instance.customize_for_csv() for instance in self.instances)
        if not self.filename:
            self.filename = '{0}{1}_{2}.csv'.format(
                self.instances[0].__class__.__name__, datetime.today().strftime('%Y%m%d%H%M%S'))
        self.output_to_console('Writing to {}\n'.format(self.filename))
        export_model_helper = ExportObjectHelper(
            self.export_plan,
            delimiter=self.delimiter,
            fields=self.instances[0].data.keys(),
            filename=self.filename,
            exception_cls=self.exception_cls)
        export_model_helper.writer.write_to_file(instances_for_csv, self.write_header)

    def output_to_console(self, text):
        """Outputs a text string to the console."""
        sys.stdout.write(text)
        sys.stdout.flush()

    def progress_to_console(self, text, index, count):
        """Outputs the progress to console while staying on one line."""
        progress = round(100 * (float(index) / float(count)))
        sys.stdout.write('{0} [{1} %] \r'.format(text, progress))
        sys.stdout.flush()
