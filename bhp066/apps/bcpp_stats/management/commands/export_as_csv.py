from django.core.management.base import BaseCommand

from ...utils import export_model_as_csv


class Command(BaseCommand):
    """A management command to exports data from a model to a csv file."""
    args = '<destination_path> <model_name>'
    help = 'Output data from a model to a destination file in CSV format'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        """Exports a model as CSV.

        Usage: python manage.py export_as_csv  <source_model> <destination_path>."""
        model_name = args[0]
        destination_path = args[1]
        export_model_as_csv('bcpp_stats', model_name, destination_path, exclude_system_fields=True,
                            additional_exclude_fields=['_community', '_title', '_description'])
        print 'Done.'
