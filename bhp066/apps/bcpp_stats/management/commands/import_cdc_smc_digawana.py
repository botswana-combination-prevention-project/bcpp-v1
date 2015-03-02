import csv
import copy
import collections

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand, CommandError

from ...models import CdcSmcDigawana


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
        system_fields = ['id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified']
        print 'importing file ' + source_path
        with open(source_path, 'r') as f:
            rows = csv.reader(f, delimiter=',')
            for i, row in enumerate(rows):
                values = {}
                if not header_row:
                    header_row = [self.strip_underscore(item) for item in copy.deepcopy(row)]
                    if [x for x, y in collections.Counter(header_row).items() if y > 1]:
                        raise TypeError('Duplicate field names detected in header_row. Got {0}'.format([x for x, y in collections.Counter(header_row).items() if y > 1]))
                else:
                    # dates are in odd formats, try to convert or fail
                    for field in CdcSmcDigawana._meta.fields:
                        if 'Date' in field.get_internal_type() and field.name not in system_fields + ['_import_datetime']:
                            if field.name in ['Visit_datetime_x', 'Contact1_DTM_x', 'Contact2_DTM_x', 'Contact3_DTM_x', 'MC_Date_x'] and row[header_row.index(field.name)]:
                                row[header_row.index(field.name)] = datetime.fromordinal(int(row[header_row.index(field.name)]))
                            elif field.name in ['referral_appt_date', 'Visit_datetime'] and row[header_row.index(field.name)]:
                                try:
                                    row[header_row.index(field.name)] = datetime.strptime(row[header_row.index(field.name)], '%m/%d/%Y')
                                except ValueError:
                                    row[header_row.index(field.name)] = datetime.strptime(row[header_row.index(field.name)], '%m/%d/%Y %I:%M:%S %p')
                            elif field.name in ['Contact1_DTM', 'Contact2_DTM', 'Contact3_DTM', 'MC_Date'] and row[header_row.index(field.name)]:
                                try:
                                    row[header_row.index(field.name)] = datetime.strptime(row[header_row.index(field.name)], '%d/%m/%y')
                                except ValueError as e:
                                    if 'day is out of range for month' in e:
                                        print '{0}. Got {1}'.format(e, row[header_row.index(field.name)])
                                        row[header_row.index(field.name)] = None
                                    else:
                                        try:
                                            row[header_row.index(field.name)] = datetime.strptime(row[header_row.index(field.name)], '%d/%m/%Y')
                                        except ValueError as e:
                                            row[header_row.index(field.name)] = datetime.strptime(row[header_row.index(field.name)], '%d/%m/%Y %I:%M:%S %p')
                            else:
                                print 'Row {0}. Unable to convert date string {1} to DateTime. Got {2}'.format(i, field.name, row[header_row.index(field.name)] or None)
                                row[header_row.index(field.name)] = None
                        if 'Integer' in field.get_internal_type() and field.name not in system_fields + ['_import_datetime', '_age_in_years']:
                            try:
                                row[header_row.index(field.name)] = int(row[header_row.index(field.name)] or None)
                            except ValueError:
                                row[header_row.index(field.name)] = None
                            except TypeError:
                                row[header_row.index(field.name)] = None
                    # populate dictionary for model.create
                    values = dict(zip(header_row, row))
                    values.update({'_title': source_path.split('/')[-1:]})
                    values.update({'_filename': source_path})
                    CdcSmcDigawana.objects.create(**values)
