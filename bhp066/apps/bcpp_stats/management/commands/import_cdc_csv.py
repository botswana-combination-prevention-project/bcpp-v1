import csv
import copy
import collections

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model


class Command(BaseCommand):

    args = '<source_path> <detsination_model>'
    help = 'Import CDC data from csv into a known model'
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
        model_name = args[1]
        model_cls = get_model('bcpp_stats', model_name)
        header_row = None
        system_fields = ['id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified']
        additional_fields = ['_community', '_title', '_import_datetime', '_description', '_filename']
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
                    for field in model_cls._meta.fields:
                        if field.name not in system_fields + additional_fields:
                            if 'Date' in field.get_internal_type() and field.name not in system_fields + ['_import_datetime']:
                                try:
                                    row[header_row.index(field.name)] = datetime.strptime(row[header_row.index(field.name)], '%Y-%m-%d')
                                except ValueError:
                                    try:
                                        row[header_row.index(field.name)] = datetime.strptime(row[header_row.index(field.name)], '%Y-%m-%d %H:%M:%S')
                                    except ValueError:
                                        print 'Row {0}. Unable to convert date string {1} to DateTime. Got {2}'.format(i, field.name, row[header_row.index(field.name)] or None)
                                        row[header_row.index(field.name)] = None
                                except IndexError as e:
                                    raise IndexError('{0}. {1}'.format(field.name, e))
                            elif 'Integer' in field.get_internal_type() and field.name not in system_fields + ['_import_datetime', '_age_in_years']:
                                try:
                                    row[header_row.index(field.name)] = int(row[header_row.index(field.name)] or None)
                                except ValueError:
                                    row[header_row.index(field.name)] = None
                                except TypeError:
                                    row[header_row.index(field.name)] = None
                                except IndexError as e:
                                    raise IndexError('{0}. {1}'.format(field.name, e))
                            elif 'Char' in field.get_internal_type() and field.name not in system_fields + ['_import_datetime', '_age_in_years']:
                                try:
                                    row[header_row.index(field.name)] = row[header_row.index(field.name)]
                                except IndexError as e:
                                    raise IndexError('{0}. {1}'.format(field.name, e))
                            elif 'Float' in field.get_internal_type() and field.name not in system_fields + ['_import_datetime', '_age_in_years']:
                                try:
                                    if row[header_row.index(field.name)]:
                                        row[header_row.index(field.name)] = float(row[header_row.index(field.name)])
                                    else:
                                        row[header_row.index(field.name)] = None
                                except ValueError as e:
                                    raise ValueError('{0}. (value={2}) {1}'.format(field.name, e, row[header_row.index(field.name)]))
                                except IndexError as e:
                                    raise IndexError('{0}. {1}'.format(field.name, e))
                            else:
                                raise TypeError('{0}. Unknown field type. Got. {1}'.format(field.name, field.get_internal_type()))
                    # populate dictionary for model.create
                    values = dict(zip(header_row, row))
                    values.update({'_title': source_path.split('/')[-1:]})
                    values.update({'_filename': source_path})
                    model_cls.objects.create(**values)
