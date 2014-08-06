import csv

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model


class Command(BaseCommand):

    args = '<model_name> <destination_path>'
    help = 'Output data from a model to a destination file in CSV format'
    option_list = BaseCommand.option_list

    def strip_underscore(self, item):
        """Returns  a string stripped of a leading or tailing underscore."""
        if item.startswith('_'):
            item = item[1:]
        if item.endswith('_'):
            item = item[:-1]
        return item

    def handle(self, *args, **options):
        model_name = args[0]
        destination_path = args[1]
        excluded_fields = ['modified', 'created', 'user_created', 'user_modified', 'hostname_created', 'hostname_modified', '_community', '_title', '_description']
        model = get_model('bcpp_stats', model_name)
        values_row = [field.name for field in model._meta.fields if field.name not in excluded_fields]
        header_row = [self.strip_underscore(x) for x in values_row]
        print 'Writing data from {0} to file {1}'.format(model_name, destination_path)
        with open(destination_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header_row)
            for row in model.objects.values_list(*values_row).order_by('id'):
                writer.writerow(row)
        print 'Done.'
