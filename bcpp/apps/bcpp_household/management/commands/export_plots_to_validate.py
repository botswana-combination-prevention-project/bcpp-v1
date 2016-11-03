import csv
import os

from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_household.models import Plot


class Command(BaseCommand):
    """Creates a csv files of 4 files containing plot list of 75, 25, 20 and 5 percent. """

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>'
    help = 'Creates a  two csv files of plot lists, 25 percent and 75 percent.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        value_attributes = ['plot_identifier', 'gps_target_lat', 'gps_target_lon', 'selected']
        backup_plots = [value_attributes]  # Plots in the 5 percent
        plot_20_pct = [value_attributes]  # Plots in the 20 percent
        plot_75_pct = [value_attributes]  # Plot in the 75 percent
        plot_25_pct = [value_attributes]  # Plot in the 25 percent
        plots = Plot.objects.filter(community=community_name)
        plot_num = plots.count()
        count = 0
        for plot in plots:
            if plot.selected == '1':
                plot_20_pct.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                plot_25_pct.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
            elif plot.selected == '2':
                backup_plots.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
                plot_25_pct.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
            else:
                plot_75_pct.append([plot.plot_identifier, plot.gps_target_lat, plot.gps_target_lon, plot.selected])
            count += 1
            print "{0} out of {1} added to a list.".format(count, plot_num)
        # File names
        community_name = community_name.title()
        filename_20_pct = str(community_name) + '_20pct.csv'
        filename_75_pct = str(community_name) + '_75pct.csv'
        filename_5_pct = str(community_name) + '_backup.csv'
        filename_25_pct = str(community_name) + '_25pct.csv'
        # Create a 20 percent plot list csv file
        file_20 = open(filename_20_pct, 'wb')
        writer = csv.writer(file_20, delimiter='|')
        writer.writerows(plot_20_pct)
        # Create a 75 percent plot list csv file
        file_75 = open(filename_75_pct, 'wb')
        writer_75_pct = csv.writer(file_75, delimiter='|')
        writer_75_pct.writerows(plot_75_pct)
        # Create a 5 percent plot list csv file
        file_5 = open(filename_5_pct, 'wb')
        writer_5_pct = csv.writer(file_5, delimiter='|')
        writer_5_pct.writerows(backup_plots)
        # Create a 25 percent plot list csv file
        file_25 = open(filename_25_pct, 'wb')
        writer_5_pct = csv.writer(file_25, delimiter='|')
        writer_5_pct.writerows(plot_25_pct)

        print " Sampling Log"
        print "4 CSV files created. Location:"
        print "Total records in {0}: {1}".format(community_name, plot_num)
        print "BHS sample 20 percent: {0}".format(len(plot_20_pct) - 1)
        print "BHS sample 25 percent: {0}".format(len(plot_25_pct) - 1)
        print "Backup, 5 percent: {0}".format(len(backup_plots) - 1)
        print "75 percent total: {0}".format(len(plot_75_pct) - 1)
        print "location of the files:"
        os.system('pwd')
