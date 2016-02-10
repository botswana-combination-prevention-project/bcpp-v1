import csv
import copy
import collections

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand, CommandError

from ...models import CdcHtcIntake


class Command(BaseCommand):

    args = '<source_path>'
    help = 'Import CDC HTC data from csv'
    option_list = BaseCommand.option_list

    def strip_underscore(self, item):
        """Returns  a string stripped of a leading or tailing underscore."""
        if item.startswith('_'):
            item = item[1:] + '2'
        if item.endswith('_'):
            item = item[:-1]
        return item

    def handle(self, *args, **options):
        source_path = args[0]
        header_row = None
        system_fields = [
            'id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified']
        print 'importing file ' + source_path
        with open(source_path, 'r') as f:
            rows = csv.reader(f, delimiter=',')
            for i, row in enumerate(rows):
                values = {}
                if not header_row:
                    header_row = [self.strip_underscore(item) for item in copy.deepcopy(row)]
                    if [x for x, y in collections.Counter(header_row).items() if y > 1]:
                        raise TypeError(
                            'Duplicate field names detected in '
                            'header_row. Got {0}'.format(
                                [x for x, y in collections.Counter(header_row).items() if y > 1]))
                else:
                    # dates are in odd formats, try to convert or fail
                    for field in CdcHtcIntake._meta.fields:
                        value = system_fields + ['_import_datetime']
                        if 'Date' in field.get_internal_type() and field.name not in value:
                            if field.name == 'DOB' and row[header_row.index(field.name)]:
                                row_val = row[header_row.index(field.name)][-2:]
                                row[header_row.index(field.name)] = datetime.strptime(
                                    row[header_row.index(field.name)][0:5] + '19' + row_val, '%d%b%Y')
                            else:
                                try:
                                    dt = datetime.strptime(row[header_row.index(field.name)], '%d%b%y')
                                    row[header_row.index(field.name)] = dt
                                except IndexError as e:
                                    print 'Field name not in header row. Got \'{0}\' ({1})'.format(field.name, e)
                                except ValueError:
                                    try:
                                        dt = datetime.strptime(
                                            row[header_row.index(field.name)][0:18], '%d%b%Y:%H:%M:%S')
                                        row[header_row.index(field.name)] = dt
                                    except ValueError:
                                        print 'Row {0}. Unable to convert date string {1} '
                                        'to DateTime. Got {2}'.format(
                                            i, field.name, row[header_row.index(field.name)] or None)
                                        row[header_row.index(field.name)] = None
                        val = system_fields + ['_import_datetime', '_age_in_years']
                        if 'Integer' in field.get_internal_type() and field.name not in val:
                            try:
                                row[header_row.index(field.name)] = int(row[header_row.index(field.name)] or None)
                            except ValueError:
                                row[header_row.index(field.name)] = None
                            except TypeError:
                                row[header_row.index(field.name)] = None
                    # populate dictionary for model.create
                    values = dict(zip(header_row, row))
                    if row[header_row.index('DOB')]:
                        values.update({'_age_in_years': relativedelta(
                            row[header_row.index('intv_dt')], row[header_row.index('DOB')]).years})
                    values.update({'_title': source_path.split('/')[-1:]})
                    values.update({'_filename': source_path})
                    CdcHtcIntake.objects.create(**values)
