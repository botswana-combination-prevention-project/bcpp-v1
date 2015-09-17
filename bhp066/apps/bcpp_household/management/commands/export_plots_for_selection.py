import csv

from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_household.models import Plot


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>'
    help = 'Creates a  csv file of plot list to be used for selection.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        plots_for_selection = []
        count = 0
        plots = Plot.objects.filter(community=community_name)
        plots_for_selection.append(['plot_identifier', 'gps_target_lat', 'gps_target_lon', 'selected'])
        for plot in plots:
            plots_for_selection.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
            count += 1
            print "plot {0} added to list. {1}/{2} added.".format(plot.plot_identifier, count, len(plots))
        # csv filename
        filename = str(community_name) + '.csv'
        # write to csv
        for_selection = open(filename, 'wb')
        writer = csv.writer(for_selection, delimiter=',')
        writer.writerows(plots_for_selection)
