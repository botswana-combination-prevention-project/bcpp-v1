import csv
import copy
import collections

from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.models import get_model

from ...utils import strip_underscore, export_model_as_csv, summarize_model_data


class Command(BaseCommand):
    """ A management command that writes the contents of a CSV file to a given model.

    If you specify the export prefix it will export the data back to a file of the
    same filename as source_path but with the export_prefix as the filename prefix.

    Usage: python manage.py import_to_csv <source_path> <detsination_model>."""
    args = '<source_path> <detsination_model> <export_prefix> <delete-existing>'
    help = 'Import CDC data from CSV into a given destinantion model'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        """Writes the contents of a CSV file to a given model."""
        source_path = args[0]
        model_name = args[1]
        try:
            export_prefix = args[2]
        except IndexError:
            export_prefix = None
        model_cls = get_model('bcpp_stats', model_name)
        try:
            if args[3] == 'delete-existing':
                model_cls.objects.all().delete()
        except IndexError:
            pass
        header_row = None
        system_fields = [
            'id', 'created', 'modified', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified']
        additional_fields = ['_community', '_title', '_import_datetime', '_description', '_filename']
        empty_fields = []  # fields in the model but not in the header row
        print 'Importing file ' + source_path
        print '  Model {1} has {0} records to start.'.format(model_cls.objects.count(), model_cls._meta.object_name)
        start_count = model_cls.objects.count()
        with open(source_path, 'r') as file_object:
            rows = csv.reader(file_object, delimiter=',')
            for i, row in enumerate(rows):
                if not header_row:
                    # set the header row list
                    header_row = [strip_underscore(item) for item in copy.deepcopy(row)]
                    # check for duplicate field names
                    if [x for x, y in collections.Counter(header_row).items() if y > 1]:
                        lst = [x for x, y in collections.Counter(header_row).items() if y > 1]
                        raise TypeError('Duplicate field names detected in header_row. Got {0}'.format(lst))
                else:
                    # confirm that the row is correctly split, e.g. formatted correctly without CR, LF etc
                    if len(header_row) != len(row):
                        raise TypeError(
                            'Header row length must be the same as the data row. '
                            'Got {0} != {1}'.format(len(header_row), len(row)))
                    for field in model_cls._meta.fields:
                        # check that field exists in the target model. If not skip it. This may occur if CSV files
                        # with partially matching fields are merged into the same model.
                        if field.name not in header_row + system_fields + additional_fields:
                            empty_fields.append(field.name)
                        else:
                            # determine the fields datatype and confirm the row value is of that data type.
                            # if the value is not of the expected datatype, raise an error.
                            # we ignore the auto-fill Edc system fields
                            if field.name not in system_fields + additional_fields:
                                try:
                                    row_val = row[header_row.index(field.name)]
                                    if not row_val or row[header_row.index(field.name)] == '.':
                                            # the cell is empty, set to None, Noticed some have '.' instead of a blank.
                                            row[header_row.index(field.name)] = None
                                    else:
                                        if 'Date' in field.get_internal_type():
                                            # model field is DateField or DateTime field
                                            try:
                                                # try to convert to a date YYYY-MM-DD or fail
                                                val = datetime.strptime(row[header_row.index(field.name)], '%Y-%m-%d')
                                                row[header_row.index(field.name)] = val
                                            except ValueError:
                                                try:
                                                    # try to convert to a date YYYY-MM-DD HH:MM:SS or fail
                                                    value = datetime.strptime(
                                                        row[header_row.index(field.name)], '%Y-%m-%d %H:%M:%S')
                                                    row[header_row.index(field.name)] = value
                                                except ValueError:
                                                    try:
                                                        # try to convert to a date YYYY-MM-DDTHH:MM:SS or
                                                        # fail (saw this in an SMC file, not quite timezone aware)
                                                        value = datetime.strptime(
                                                            row[header_row.index(field.name)], '%Y-%m-%dT%H:%M:%S')
                                                        row[header_row.index(field.name)] = value
                                                    except ValueError:
                                                        try:
                                                            # this is the bad date e.g. 23NOV13 and assume century
                                                            value = datetime.strptime(
                                                                row[header_row.index(field.name)], '%d%b%y')
                                                            row[header_row.index(field.name)] = value
                                                        except ValueError as error_msg:
                                                            # failed so print a warning and show the value
                                                            x = row[header_row.index(field.name)]
                                                            raise ValueError(
                                                                'In {4} Row {0}. Unable to convert date string {1} '
                                                                'to DateTime. Got {2}. {3}.'.format(
                                                                    i, field.name, x or None, error_msg, model_name))
                                        elif 'Integer' in field.get_internal_type():
                                            # model field is an IntegerField
                                            try:
                                                row[header_row.index(field.name)] = int(
                                                    row[header_row.index(field.name)] or None)
                                            except ValueError as error_mgs:
                                                # conversion of cell value to integer failed
                                                x = row[header_row.index(field.name)]
                                                raise ValueError('In {3}, {0}. (value={2}) {1}'.format(
                                                    field.name, error_mgs, x, model_name))
                                        elif 'Char' in field.get_internal_type():
                                            # model field is an CharField
                                            # accept anything that is in the cell
                                            # row[header_row.index(field.name)] = row[header_row.index(field.name)]
                                            row[header_row.index(field.name)] = ''.join(
                                                [i if ord(i) < 128 else ' ' for i in row[header_row.index(field.name)]])
                                        elif 'Float' in field.get_internal_type():
                                            # model field is an FloatField
                                            try:
                                                row[header_row.index(field.name)] = float(
                                                    row[header_row.index(field.name)])
                                            except ValueError as error_mgs:
                                                # conversion of cell value to integer failed
                                                x = row[header_row.index(field.name)]
                                                raise ValueError('in {3}, {0}. (value={2}) {1}'.format(
                                                    field.name, error_mgs, x, model_name))
                                        else:
                                            # model field is an of an unhandled type, so fail
                                            raise TypeError('In {1}, {0}. Unknown field type. Got. {1}'.format(
                                                field.name, field.get_internal_type(), model_name))
                                except IndexError as error_mgs:
                                    # field name is not in the header!
                                    raise IndexError('{0}. {1}'.format(field.name, error_mgs))
                    # populate dictionary for model.create
                    values = dict(zip(header_row, row))
                    # add some system values
                    values.update({'_title': source_path.split('/')[-1:]})
                    values.update({'_filename': source_path})
                    # add the row to the model
                    model_cls.objects.create(**values)
        # we want to warn of model fields that were not known to the CSV file, maybe we didn't expect this.
        # de-duplicate and sort the list and print out the warnings, if any.
        empty_fields = list(set(empty_fields))
        empty_fields.sort()
        for empty_field in empty_fields:
            print '  not updating {0}.'.format(empty_field)
        # Done
        # Print a description/summary of the process
        print '  Detected {0} rows by {1} columns in the source CSV file (not including the header_row).'.format(
            i, len(header_row))
        print '  Imported {0} records into model {1} from the source CSV file.\n'.format(
            model_cls.objects.count() - start_count, model_cls._meta.object_name)
        summarize_model_data(model_cls, header_row)
        if export_prefix:
            dest = '/'.join(source_path.split('/')[:-1]) + '/' + export_prefix + '-' + source_path.split('/')[-1:][0]
            export_model_as_csv(
                'bcpp_stats', model_name, dest, exclude_system_fields=True,
                additional_exclude_fields=['_community', '_title', '_description'])
        print '  Done.'
