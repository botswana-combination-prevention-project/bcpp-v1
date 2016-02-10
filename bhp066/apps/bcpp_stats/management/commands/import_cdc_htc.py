import csv

from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from ...models import CdcHtc


class Command(BaseCommand):

    args = '<source_path>'
    help = 'Import CDC HTC data from csv'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        source_path = args[0]
        header_row = []

        print 'importing file ' + source_path
        with open(source_path, 'r') as f:
            values = {}
            rows = csv.reader(f, delimiter=',')
            for i, row in enumerate(rows):
                values = {}
                if not header_row:
                    header_row = row
                    for field in CdcHtc._meta.fields:
                        value = [
                            'id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created',
                            'hostname_modified']
                        if field.name not in value and field.name not in header_row:
                            header_row.append(field.name)
                else:
                    # dates are in odd formats, try to convert or fail
                    for field in CdcHtc._meta.fields:
                        _val = ['created', 'modified', '_import_datetime']
                        if 'Date' in field.get_internal_type() and field.name not in _val:
                            try:
                                dt = datetime.strptime(row[header_row.index(field.name)], '%d%b%y')
                                row[header_row.index(field.name)] = dt
                            except IndexError:
                                print field.name
                            except ValueError:
                                try:
                                    dt = datetime.strptime(row[header_row.index(field.name)][0:18], '%d%b%Y:%H:%M:%S')
                                    row[header_row.index(field.name)] = dt
                                except ValueError:
                                    print 'Row {0}. Unable to convert date string {1} to DateTime. '
                                    'Got {2}'.format(i, field.name, row[header_row.index(field.name)] or None)
                                    row[header_row.index(field.name)] = None
                        value = ['created', 'modified', '_import_datetime']
                        if 'Integer' in field.get_internal_type() and field.name not in value:
                            try:
                                row[header_row.index(field.name)] = int(row[header_row.index(field.name)])
                            except ValueError:
                                row[header_row.index(field.name)] = None
                    # populate dictionary for model.create
                    values = dict(zip(header_row, row))
                    values.update({'_community': row[header_row.index('Community_Name')].lower()})
                    values.update({'_title': source_path.split('/')[-1:]})
                    values.update({'_filename': source_path})
                    CdcHtc.objects.create(**values)
