import csv

from django.db.models import get_model

from .strip_underscore import strip_underscore


def export_model_as_csv(app_label, model_name, destination_path, exclude_system_fields=None,
                        additional_exclude_fields=None):
    """Exports a model to CSV without decrypting encrypted fields.

    If the destination file exists it will be overwritten.

    Keywords:
        * exclude_system_fields: do not include Edc system fields from model subclass BaseModel in the
          export file (default=None)
        * additional_exclude_fields: a list of field names to exclude from the CSV file (default=None)
    """
    excluded_fields = []
    additional_exclude_fields = additional_exclude_fields or []
    if exclude_system_fields:
        excluded_fields = ['modified', 'created', 'user_created', 'user_modified', 'hostname_created',
                           'hostname_modified'] + additional_exclude_fields
    model = get_model(app_label, model_name)
    values_row = [field.name for field in model._meta.fields if field.name not in excluded_fields]
    header_row = [strip_underscore(x) for x in values_row]
    # print 'Writing data from {0} to file {1}'.format(model_name, destination_path)
    with open(destination_path, 'w') as file_object:
        writer = csv.writer(file_object)
        writer.writerow(header_row)
        for row in model.objects.values_list(*values_row).order_by('id'):
            writer.writerow(row)
    with open(destination_path, 'r') as file_object:
        rows = [row for row in csv.reader(file_object, delimiter=',')]
    print ('  Exported {0} lines (not including the header_row) '
           'to {2} columns from model {1}.').format(len(rows) - 1, app_label + '.' + model_name, len(rows[0]))
    print '  New CSV file is {0}'.format(destination_path)
