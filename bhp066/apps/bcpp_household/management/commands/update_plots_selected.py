import os

from django.core.management.base import BaseCommand, CommandError

from apps.bcpp_household.models import Plot


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community_name e.g otse>, <file_path e.g /home/django/>'
    help = 'Prints a report that shows reconciliation statistics of plot lists belonging to 75%, 20%, 5%.'

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        file_path = str(args[1]) + str(community_name.title())
        file_75_list = file_path + '_75pct.csv'
        file_20_list = file_path + '_20pct.csv'
        file_5_list = file_path + '_backup.csv'
        if not (os.path.exists(file_75_list) and os.path.exists(file_20_list) and os.path.exists(file_5_list)):
            raise IOError("Files do not exist in the path: {0}.", format(args[1]))
        else:
            plots_75_list = open(file_75_list, 'r')
            lines_75 = plots_75_list.readlines()
            lines_75.pop(0)
            plot_identifiers_75 = []
            for line in lines_75:
                line = line.split(',')
                plot_identifier = line[-4][1:-1]
                plot_identifiers_75.append(plot_identifier)

            # TODO update the 75 percent plots


            # The 20 percent plot list
            plots_20_list = open(file_20_list, 'r')
            lines_20 = plots_20_list.readlines()
            plot_identifiers_20 = []
            lines_20.pop(0)
            for line in lines_20:
                line = line.split(',')
                plot_identifier = line[-4][1:-1]
                plot_identifiers_20.append(plot_identifier)

            # TODO update the 20 percent plots

            # The 5 percent plot list
            plots_5_list = open(file_5_list, 'r')
            lines_5 = plots_5_list.readlines()
            lines_5.pop(0)
            plot_identifiers_5 = []
            for line in lines_5:
                line = line.split(',')
                plot_identifier = line[-4][1:-1]
                plot_identifiers_5.append(plot_identifier)

            # TODO update the 5 percent plots
