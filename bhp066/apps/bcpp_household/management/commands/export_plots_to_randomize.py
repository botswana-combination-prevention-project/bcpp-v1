import csv

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from apps.bcpp_household.models import Plot


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>'
    help = 'Creates a  two csv files of plot lists, 25 percent and 75 percent.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        filename = str(community_name) + '_to_randomize.csv'
        plots_file = open(filename, 'wb')
        plots_to_randomize = []
        plots = Plot.objects.all()
        add_plots = 0
        if not plots[0].community == str(community_name):
            raise ValidationError("The plots in this database does not belong to the community {0} you passed in kwrgs. expecting {1}: ".format(community_name, plots[0].community))
        else:
            plots_to_randomize.append(['plot_identifier', 'gps_target_lat', 'gps_target_lon', 'selected', 'id'])
            for plot in plots:
                plots_to_randomize.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected, plot.id])
                add_plots += 1
                print "Adding plot {0} to list to be exported. out of {1}".format(add_plots, plots.count())
            writer = csv.writer(plots_file)
            writer.writerows(plots_to_randomize)
            print "Total of {0} plot exported. plot list file name {1}.".format(len(plots_to_randomize) - 1, filename)
            print "Success!!!"
